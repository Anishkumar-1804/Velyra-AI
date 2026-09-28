import json
import csv
import io
from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.orm import Session as DBSession

from backend.app.database import get_db
from backend.app.config import settings
from backend.app.models.settings import UserSettings
from backend.app.models.attempt import SessionAttempt
from backend.app.models.conversation import ConversationTurn
from backend.app.models.evaluation import Evaluation
from backend.app.models.correction import Correction, VocabularyFeedback
from backend.app.schemas.settings import SettingsUpdate, SettingsResponse

router = APIRouter(prefix="/settings", tags=["Settings"])


@router.get("", response_model=SettingsResponse)
def get_user_settings(db: DBSession = Depends(get_db)):
    """Get active application settings."""
    user_setting = db.query(UserSettings).filter(UserSettings.id == 1).first()
    if not user_setting:
        user_setting = UserSettings(
            id=1,
            stt_model=settings.STT_MODEL,
            llm_model=settings.LLM_MODEL,
            tts_voice=settings.TTS_VOICE,
            tts_speed=str(settings.TTS_SPEED),
            input_mode="auto_vad",
            auto_play_audio="true",
            store_audio="false"
        )
        db.add(user_setting)
        db.commit()
        db.refresh(user_setting)

    import torch
    cuda_avail = torch.cuda.is_available()
    available_devices = ["cpu"]
    if cuda_avail:
        available_devices.append("cuda")

    return {
        "stt_model": user_setting.stt_model,
        "llm_model": user_setting.llm_model,
        "tts_voice": user_setting.tts_voice,
        "tts_speed": user_setting.tts_speed,
        "input_mode": user_setting.input_mode,
        "auto_play_audio": user_setting.auto_play_audio,
        "store_audio": user_setting.store_audio,
        "available_devices": available_devices,
        "current_device": "cuda" if cuda_avail else "cpu",
        "is_cuda_available": cuda_avail
    }


@router.put("", response_model=SettingsResponse)
def update_user_settings(updates: SettingsUpdate, db: DBSession = Depends(get_db)):
    """Update settings in database."""
    user_setting = db.query(UserSettings).filter(UserSettings.id == 1).first()
    if not user_setting:
        user_setting = UserSettings(id=1)
        db.add(user_setting)

    if updates.stt_model is not None:
        user_setting.stt_model = updates.stt_model
    if updates.llm_model is not None:
        user_setting.llm_model = updates.llm_model
    if updates.tts_voice is not None:
        user_setting.tts_voice = updates.tts_voice
    if updates.tts_speed is not None:
        user_setting.tts_speed = updates.tts_speed
    if updates.input_mode is not None:
        user_setting.input_mode = updates.input_mode
    if updates.auto_play_audio is not None:
        user_setting.auto_play_audio = updates.auto_play_audio
    if updates.store_audio is not None:
        user_setting.store_audio = updates.store_audio

    db.commit()
    db.refresh(user_setting)
    return get_user_settings(db)


@router.get("/export/json")
def export_progress_json(db: DBSession = Depends(get_db)):
    """Export complete real session logs, full transcripts, corrections, and evaluations as JSON."""
    attempts = db.query(SessionAttempt).order_by(SessionAttempt.started_at.desc()).all()
    export_data = []

    for att in attempts:
        sess = att.session
        genre = sess.genre if sess else None
        unit = sess.unit if sess else None
        turns = (
            db.query(ConversationTurn)
            .filter(ConversationTurn.attempt_id == att.id)
            .order_by(ConversationTurn.turn_index.asc())
            .all()
        )
        eval_rec = db.query(Evaluation).filter(Evaluation.attempt_id == att.id).first()
        corrections = (
            db.query(Correction).filter(Correction.evaluation_id == eval_rec.id).all()
            if eval_rec else []
        )
        vocab_items = (
            db.query(VocabularyFeedback).filter(VocabularyFeedback.evaluation_id == eval_rec.id).all()
            if eval_rec else []
        )

        attempt_dict = {
            "attempt_id": att.id,
            "session_id": att.session_id,
            "session_title": sess.title if sess else "Speaking Scenario",
            "genre_title": genre.title if genre else "General",
            "unit_title": unit.title if unit else "General",
            "difficulty": sess.difficulty if sess else "Intermediate",
            "target_cefr": sess.cefr_level if sess else "B1",
            "started_at": att.started_at.isoformat() if att.started_at else None,
            "completed_at": att.completed_at.isoformat() if att.completed_at else None,
            "status": att.status,
            "duration_seconds": att.session_duration,
            "total_speaking_duration_seconds": att.total_speaking_duration,
            "turn_count": att.turn_count,
            "user_turn_count": att.user_turn_count,
            "ai_turn_count": att.ai_turn_count,
            "turns": [
                {
                    "turn_index": t.turn_index,
                    "speaker": t.speaker,
                    "transcript": t.transcript,
                    "audio_duration_seconds": t.audio_duration,
                    "confidence": t.confidence,
                    "filler_count": t.filler_count,
                    "detected_fillers": t.detected_fillers or [],
                    "pause_count": t.pause_count,
                    "created_at": t.created_at.isoformat() if t.created_at else None
                } for t in turns
            ],
            "evaluation": {
                "overall_score": eval_rec.overall_score,
                "fluency": eval_rec.fluency,
                "accuracy": eval_rec.accuracy,
                "grammar": eval_rec.grammar,
                "vocabulary": eval_rec.vocabulary,
                "pronunciation_estimate": eval_rec.pronunciation_estimate,
                "comprehension": eval_rec.comprehension,
                "sentence_formation": eval_rec.sentence_formation,
                "naturalness": eval_rec.naturalness,
                "conversation_relevance": eval_rec.conversation_relevance,
                "confidence_estimate": eval_rec.confidence_estimate,
                "estimated_cefr": eval_rec.estimated_cefr,
                "cefr_reasoning": eval_rec.cefr_reasoning,
                "total_speaking_time": eval_rec.total_speaking_time,
                "avg_response_words": eval_rec.avg_response_words,
                "filler_count": eval_rec.filler_count,
                "filler_rate": eval_rec.filler_rate,
                "most_used_filler": eval_rec.most_used_filler,
                "filler_breakdown": eval_rec.filler_breakdown or {},
                "repetition_analysis": eval_rec.repetition_analysis or {},
                "strengths": eval_rec.strengths or [],
                "improvements": eval_rec.improvements or [],
                "naturalness_tips": eval_rec.naturalness_tips or [],
                "recommendations": eval_rec.recommendations or [],
                "corrections": [
                    {
                        "user_said": c.user_said,
                        "better_version": c.better_version,
                        "issue": c.issue,
                        "explanation": c.explanation,
                        "category": c.category
                    } for c in corrections
                ],
                "vocabulary_feedback": [
                    {
                        "word_used": v.word_used,
                        "better_alternative": v.better_alternative,
                        "reason": v.reason,
                        "example": v.example
                    } for v in vocab_items
                ]
            } if eval_rec else None
        }
        export_data.append(attempt_dict)

    json_content = json.dumps(export_data, indent=2, ensure_ascii=False)
    return Response(
        content=json_content,
        media_type="application/json",
        headers={
            "Content-Disposition": "attachment; filename=angiyam_practice_history.json",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )


@router.get("/export/csv")
def export_progress_csv(db: DBSession = Depends(get_db)):
    """Export comprehensive practice records and granular scores as CSV."""
    attempts = db.query(SessionAttempt).order_by(SessionAttempt.started_at.desc()).all()
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Comprehensive header columns
    writer.writerow([
        "Attempt ID",
        "Genre",
        "Unit",
        "Session Title",
        "Difficulty",
        "Target CEFR",
        "Date & Time",
        "Status",
        "Duration (s)",
        "Total Turns",
        "User Turns",
        "Speaking Time (s)",
        "Overall Score",
        "Estimated CEFR",
        "Fluency",
        "Accuracy",
        "Grammar",
        "Vocabulary",
        "Pronunciation Estimate",
        "Naturalness",
        "Filler Count",
        "Filler Rate (/min)",
        "Top Filler",
        "Total Corrections",
        "Key Strengths",
        "Key Improvements"
    ])

    for att in attempts:
        sess = att.session
        genre = sess.genre if sess else None
        unit = sess.unit if sess else None
        eval_rec = db.query(Evaluation).filter(Evaluation.attempt_id == att.id).first()
        corrections_count = (
            db.query(Correction).filter(Correction.evaluation_id == eval_rec.id).count()
            if eval_rec else 0
        )

        strengths_str = "; ".join(eval_rec.strengths) if eval_rec and eval_rec.strengths else ""
        improvements_str = "; ".join(eval_rec.improvements) if eval_rec and eval_rec.improvements else ""

        writer.writerow([
            att.id,
            genre.title if genre else "General",
            unit.title if unit else "General",
            sess.title if sess else "Speaking Session",
            sess.difficulty if sess else "Intermediate",
            sess.cefr_level if sess else "B1",
            att.started_at.strftime("%Y-%m-%d %H:%M:%S") if att.started_at else "",
            att.status,
            round(att.session_duration, 1),
            att.turn_count,
            att.user_turn_count,
            round(att.total_speaking_duration, 1),
            eval_rec.overall_score if eval_rec else "N/A",
            eval_rec.estimated_cefr if eval_rec else "N/A",
            eval_rec.fluency if eval_rec else "N/A",
            eval_rec.accuracy if eval_rec else "N/A",
            eval_rec.grammar if eval_rec else "N/A",
            eval_rec.vocabulary if eval_rec else "N/A",
            eval_rec.pronunciation_estimate if eval_rec else "N/A",
            eval_rec.naturalness if eval_rec else "N/A",
            eval_rec.filler_count if eval_rec else 0,
            eval_rec.filler_rate if eval_rec else 0.0,
            eval_rec.most_used_filler if (eval_rec and eval_rec.most_used_filler) else "None",
            corrections_count,
            strengths_str,
            improvements_str
        ])

    return Response(
        content=output.getvalue(),
        media_type="text/csv",
        headers={
            "Content-Disposition": "attachment; filename=angiyam_progress.csv",
            "Access-Control-Expose-Headers": "Content-Disposition"
        }
    )


@router.delete("/reset")
def reset_all_progress(db: DBSession = Depends(get_db)):
    """Delete all session attempts and evaluation history while preserving curriculum."""
    db.query(Correction).delete()
    db.query(VocabularyFeedback).delete()
    db.query(Evaluation).delete()
    db.query(ConversationTurn).delete()
    db.query(SessionAttempt).delete()
    db.commit()
    return {"message": "All practice history and evaluations successfully cleared."}
