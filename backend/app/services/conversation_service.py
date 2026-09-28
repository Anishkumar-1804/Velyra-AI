import logging
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from sqlalchemy.orm import Session as DBSession

from backend.app.models.session import Session
from backend.app.models.attempt import SessionAttempt
from backend.app.models.conversation import ConversationTurn
from backend.app.models.unit import Unit
from backend.app.models.genre import Genre
from backend.app.models.settings import UserSettings
from backend.app.prompts.global_controller import build_system_prompt
from backend.app.prompts.session_prompt import format_conversation_history, build_guard_regeneration_prompt
from backend.app.services.stt_service import stt_service
from backend.app.services.llm_service import llm_service
from backend.app.services.session_guard import session_guard
from backend.app.services.tts_service import tts_service
from backend.app.utils.audio import detect_filler_words, estimate_speech_duration_from_words

logger = logging.getLogger("angiyam.conversation")


class ConversationService:
    """
    Manages live multi-turn conversational state, pipeline flow, session progress, and stage tracking.
    """
    def start_session(self, db: DBSession, session_id: int) -> Dict[str, Any]:
        """Initialize a new speaking attempt and generate opening AI turn."""
        session = db.query(Session).filter(Session.id == session_id).first()
        if not session:
            raise ValueError(f"Session with id {session_id} not found.")

        # Create new session attempt
        attempt = SessionAttempt(
            session_id=session.id,
            status="ACTIVE",
            current_stage=0,
            turn_count=0,
            user_turn_count=0,
            ai_turn_count=1,
            last_ai_turn=session.opening_message,
            started_at=datetime.utcnow()
        )
        db.add(attempt)
        db.flush()

        # Fetch active voice settings from database
        user_setting = db.query(UserSettings).filter(UserSettings.id == 1).first()
        voice = user_setting.tts_voice if user_setting and user_setting.tts_voice else settings.TTS_VOICE
        speed = float(user_setting.tts_speed) if user_setting and user_setting.tts_speed else settings.TTS_SPEED

        # Create opening AI conversation turn (Turn 0)
        ai_audio_url = tts_service.generate_speech(session.opening_message, voice=voice, speed=speed)
        turn = ConversationTurn(
            attempt_id=attempt.id,
            turn_index=0,
            speaker="ai",
            transcript=session.opening_message,
            audio_url=ai_audio_url,
            audio_duration=estimate_speech_duration_from_words(session.opening_message),
            confidence=1.0,
            filler_count=0,
            detected_fillers=[],
            pause_count=0
        )
        db.add(turn)
        db.commit()
        db.refresh(attempt)

        stages = session.conversation_stages or []
        total_stages = len(stages) if stages else 5
        suggested_response = llm_service.generate_suggested_response(session.scenario, session.opening_message, session.user_role)

        return {
            "attempt_id": attempt.id,
            "session_id": session.id,
            "status": attempt.status,
            "opening_message": session.opening_message,
            "ai_role": session.ai_role,
            "user_role": session.user_role,
            "scenario": session.scenario,
            "target_turns": session.target_turns,
            "current_stage": 0,
            "total_stages": total_stages,
            "audio_url": ai_audio_url,
            "suggested_response": suggested_response
        }


    def process_user_turn(
        self,
        db: DBSession,
        attempt_id: int,
        audio_bytes: Optional[bytes] = None,
        raw_transcript: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Full live speech pipeline:
        Audio -> STT -> Turn Record -> Prompt Controller -> LLM -> Session Guard -> Stage Advancement -> TTS -> AI Turn Record.
        """
        attempt = db.query(SessionAttempt).filter(SessionAttempt.id == attempt_id).first()
        if not attempt:
            raise ValueError(f"Attempt with id {attempt_id} not found.")

        session = attempt.session
        unit = session.unit
        genre = session.genre

        # 1. Speech-to-Text / Transcript Processing
        user_text = ""
        audio_duration = 0.0
        confidence = 0.95
        filler_count = 0
        detected_fillers = []
        pause_count = 0

        if audio_bytes and len(audio_bytes) > 0:
            stt_result = stt_service.transcribe_audio(audio_bytes)
            user_text = stt_result["transcript"].strip()
            audio_duration = stt_result["duration"]
            confidence = stt_result["confidence"]
            filler_count = stt_result["filler_count"]
            detected_fillers = stt_result["detected_fillers"]
            pause_count = stt_result["pause_count"]

        # If audio transcription was empty or client provided live transcript
        if not user_text and raw_transcript and raw_transcript.strip():
            user_text = raw_transcript.strip()
            if audio_duration <= 0.0:
                audio_duration = estimate_speech_duration_from_words(user_text)
            filler_count, detected_fillers, _ = detect_filler_words(user_text)

        # If user spoke nothing or silence
        is_silence = not user_text or user_text in ["[Silence / Unclear Audio]", "[Silence]", ""] or len(user_text.strip()) < 2
        if is_silence:
            user_text = "[No speech detected]"

        # 2. Record User Turn
        next_turn_idx = attempt.turn_count + 1
        user_turn = ConversationTurn(
            attempt_id=attempt.id,
            turn_index=next_turn_idx,
            speaker="user",
            transcript=user_text,
            audio_duration=audio_duration,
            confidence=confidence,
            filler_count=filler_count,
            detected_fillers=detected_fillers,
            pause_count=pause_count
        )
        db.add(user_turn)
        db.flush()

        # Update attempt stats
        attempt.turn_count += 1
        if not is_silence:
            attempt.user_turn_count += 1
            attempt.total_speaking_duration += audio_duration
            attempt.last_user_turn = user_text

        # 3. Determine current conversation stage
        stages = session.conversation_stages or ["1. Beginning", "2. Exploration", "3. Conclusion"]
        stage_idx = min(attempt.current_stage, len(stages) - 1)
        current_stage_name = stages[stage_idx]
        stage_objective = f"Advance the active scenario goal: {stages[stage_idx]}"

        # 4. Handle Silence vs LLM Response Generation
        if is_silence:
            # When silence occurs, gently ask the user to say something
            import random
            silence_prompts = [
                "I didn't quite catch that. Could you please say that again?",
                "I'm listening! Whenever you're ready, feel free to speak.",
                "Take your time! What would you like to say?",
            ]
            ai_response = random.choice(silence_prompts)
            is_valid = True
        else:
            # Construct System Prompt with Global Controller
            system_prompt = build_system_prompt(
                genre_title=genre.title if genre else "Daily Conversation",
                unit_title=unit.title if unit else "General",
                session_title=session.title,
                scenario=session.scenario,
                ai_role=session.ai_role,
                user_role=session.user_role,
                current_stage_name=current_stage_name,
                stage_objective=stage_objective,
                allowed_topics=session.allowed_topics or [],
                forbidden_topics=session.forbidden_topics or [],
                target_level=session.cefr_level
            )

            # Fetch past turn history (up to 8 turns)
            turns_query = (
                db.query(ConversationTurn)
                .filter(ConversationTurn.attempt_id == attempt.id)
                .order_by(ConversationTurn.turn_index.asc())
                .all()
            )
            turn_history = [{"speaker": t.speaker, "transcript": t.transcript} for t in turns_query]
            messages = format_conversation_history(turn_history, max_turns=8)

            # LLM Response Generation + Session Guard Loop
            ai_response = llm_service.generate_chat_response(system_prompt, messages)
            is_valid, violation_reason = session_guard.validate_response(
                ai_response=ai_response,
                user_message=user_text,
                ai_role=session.ai_role,
                scenario=session.scenario,
                allowed_topics=session.allowed_topics or [],
                forbidden_topics=session.forbidden_topics or []
            )

            # Guard Regeneration Attempt
            regenerations = 0
            while not is_valid and regenerations < session_guard.max_regenerations:
                regenerations += 1
                logger.warning(f"[Guard] Violation: {violation_reason}. Triggering regeneration #{regenerations}...")
                regen_prompt = build_guard_regeneration_prompt(
                    original_response=ai_response,
                    violation_reason=violation_reason or "Off-topic drift",
                    ai_role=session.ai_role,
                    scenario=session.scenario
                )
                regen_messages = messages + [{"role": "system", "content": regen_prompt}]
                ai_response = llm_service.generate_chat_response(system_prompt, regen_messages)
                is_valid, violation_reason = session_guard.validate_response(
                    ai_response=ai_response,
                    user_message=user_text,
                    ai_role=session.ai_role,
                    scenario=session.scenario,
                    allowed_topics=session.allowed_topics or [],
                    forbidden_topics=session.forbidden_topics or []
                )

            if not is_valid:
                logger.warning(f"[Guard] Guard fallback applied after {regenerations} retries.")
                ai_response = session_guard.get_safe_stage_fallback(
                    ai_role=session.ai_role,
                    scenario=session.scenario,
                    current_stage_name=current_stage_name,
                    user_message=user_text
                )

            # Advance stage only on actual user turns
            if attempt.user_turn_count > 0 and attempt.user_turn_count % 1 == 0:
                if attempt.current_stage < len(stages) - 1:
                    attempt.current_stage += 1

        is_completed = False
        target_turns = session.target_turns or 6
        if attempt.user_turn_count >= target_turns or attempt.current_stage >= len(stages) - 1:
            if attempt.user_turn_count >= 4:
                is_completed = True
                attempt.status = "COMPLETED"
                attempt.completed_at = datetime.utcnow()

        # 8. Generate TTS Audio for AI Response using active database voice setting
        user_setting = db.query(UserSettings).filter(UserSettings.id == 1).first()
        voice = user_setting.tts_voice if user_setting and user_setting.tts_voice else settings.TTS_VOICE
        speed = float(user_setting.tts_speed) if user_setting and user_setting.tts_speed else settings.TTS_SPEED

        ai_audio_url = tts_service.generate_speech(ai_response, voice=voice, speed=speed)

        # 9. Record AI Turn
        ai_turn_idx = user_turn.turn_index + 1
        ai_turn = ConversationTurn(
            attempt_id=attempt.id,
            turn_index=ai_turn_idx,
            speaker="ai",
            transcript=ai_response,
            audio_url=ai_audio_url,
            audio_duration=estimate_speech_duration_from_words(ai_response),
            confidence=1.0,
            filler_count=0,
            detected_fillers=[],
            pause_count=0
        )
        db.add(ai_turn)

        attempt.turn_count += 1
        attempt.ai_turn_count += 1
        attempt.last_ai_turn = ai_response

        # Calculate session elapsed time
        if attempt.started_at:
            delta = (datetime.utcnow() - attempt.started_at).total_seconds()
            attempt.session_duration = round(delta, 1)

        db.commit()
        db.refresh(user_turn)
        db.refresh(ai_turn)
        db.refresh(attempt)

        suggested_response = llm_service.generate_suggested_response(session.scenario, ai_response, session.user_role)

        return {
            "user_turn": {
                "id": user_turn.id,
                "attempt_id": user_turn.attempt_id,
                "turn_index": user_turn.turn_index,
                "speaker": user_turn.speaker,
                "transcript": user_turn.transcript,
                "audio_url": user_turn.audio_url,
                "audio_duration": user_turn.audio_duration,
                "confidence": user_turn.confidence,
                "filler_count": user_turn.filler_count,
                "detected_fillers": user_turn.detected_fillers or [],
                "pause_count": user_turn.pause_count,
                "created_at": user_turn.created_at
            },
            "ai_turn": {
                "id": ai_turn.id,
                "attempt_id": ai_turn.attempt_id,
                "turn_index": ai_turn.turn_index,
                "speaker": ai_turn.speaker,
                "transcript": ai_turn.transcript,
                "audio_url": ai_turn.audio_url,
                "audio_duration": ai_turn.audio_duration,
                "confidence": ai_turn.confidence,
                "filler_count": 0,
                "detected_fillers": [],
                "pause_count": 0,
                "created_at": ai_turn.created_at
            },
            "current_stage": attempt.current_stage,
            "total_stages": len(stages),
            "turn_count": attempt.turn_count,
            "is_completed": is_completed,
            "session_status": attempt.status,
            "session_guard_passed": is_valid,
            "ai_audio_url": ai_audio_url,
            "suggested_response": suggested_response
        }


    def generate_silence_nudge(self, db: DBSession, attempt_id: int) -> Dict[str, Any]:
        """Generate a gentle in-character nudge when prolonged silence is detected."""
        attempt = db.query(SessionAttempt).filter(SessionAttempt.id == attempt_id).first()
        if not attempt:
            raise ValueError(f"Attempt with id {attempt_id} not found.")

        session = attempt.session
        nudge_text = llm_service.get_silence_nudge(session.ai_role, session.scenario)

        user_setting = db.query(UserSettings).filter(UserSettings.id == 1).first()
        voice = user_setting.tts_voice if user_setting and user_setting.tts_voice else settings.TTS_VOICE
        speed = float(user_setting.tts_speed) if user_setting and user_setting.tts_speed else settings.TTS_SPEED

        audio_url = tts_service.generate_speech(nudge_text, voice=voice, speed=speed)
        return {
            "nudge_text": nudge_text,
            "audio_url": audio_url
        }


conversation_service = ConversationService()

