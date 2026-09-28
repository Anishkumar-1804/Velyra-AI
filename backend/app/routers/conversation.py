import logging
from typing import Optional
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session as DBSession

from backend.app.database import get_db
from backend.app.schemas.conversation import (
    StartSessionRequest,
    StartSessionResponse,
    UserTurnResponse,
    TurnResponse
)
from backend.app.services.conversation_service import conversation_service
from backend.app.models.attempt import SessionAttempt
from backend.app.models.conversation import ConversationTurn

logger = logging.getLogger("angiyam.routers.conversation")
router = APIRouter(prefix="/conversation", tags=["Conversation"])


@router.post("/start", response_model=StartSessionResponse)
def start_session(request: StartSessionRequest, db: DBSession = Depends(get_db)):
    """Start a speaking session attempt and receive opening AI dialogue with voice audio."""
    try:
        return conversation_service.start_session(db, request.session_id)
    except Exception as e:
        logger.error(f"Error starting session: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/turn/audio")
async def process_audio_turn(
    attempt_id: int = Form(...),
    audio_file: UploadFile = File(...),
    transcript: Optional[str] = Form(None),
    db: DBSession = Depends(get_db)
):
    """
    Process spoken user audio turn:
    Receives microphone audio -> Transcribes via faster-whisper -> Injects Global Controller ->
    Generates in-character LLM response -> Passes Session Guard -> Produces Indian English TTS.
    """
    try:
        audio_bytes = await audio_file.read()
        result = conversation_service.process_user_turn(
            db=db,
            attempt_id=attempt_id,
            audio_bytes=audio_bytes,
            raw_transcript=transcript
        )
        return result
    except Exception as e:
        logger.error(f"Error processing audio turn: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/turn/text")
def process_text_turn(
    attempt_id: int = Form(...),
    transcript: str = Form(...),
    db: DBSession = Depends(get_db)
):
    """Process a user text turn (Push-to-talk / Dev Audio Mode)."""
    try:
        result = conversation_service.process_user_turn(
            db=db,
            attempt_id=attempt_id,
            raw_transcript=transcript
        )
        return result
    except Exception as e:
        logger.error(f"Error processing text turn: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/attempt/{attempt_id}/end")
def end_session_attempt(attempt_id: int, db: DBSession = Depends(get_db)):
    """Explicitly conclude an active speaking session and trigger evaluation readiness."""
    attempt = db.query(SessionAttempt).filter(SessionAttempt.id == attempt_id).first()
    if not attempt:
        raise HTTPException(status_code=404, detail="Attempt not found")
    
    attempt.status = "COMPLETED"
    db.commit()
    return {"message": "Session marked as COMPLETED", "attempt_id": attempt.id}


@router.post("/attempt/{attempt_id}/nudge")
def get_silence_nudge(attempt_id: int, db: DBSession = Depends(get_db)):
    """Generate in-character silence nudge when user has not spoken."""
    try:
        return conversation_service.generate_silence_nudge(db, attempt_id)
    except Exception as e:
        logger.error(f"Error generating silence nudge: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/attempt/{attempt_id}/turns")
def get_attempt_turns(attempt_id: int, db: DBSession = Depends(get_db)):
    """Retrieve full transcript turns for an attempt."""
    turns = (
        db.query(ConversationTurn)
        .filter(ConversationTurn.attempt_id == attempt_id)
        .order_by(ConversationTurn.turn_index.asc())
        .all()
    )
    return turns

