from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from backend.app.database import get_db
from backend.app.schemas.session import SessionDetail
from backend.app.services.curriculum_service import curriculum_service

router = APIRouter(prefix="/sessions", tags=["Sessions"])


@router.get("/{session_id}", response_model=SessionDetail)
def get_session(session_id: int, db: DBSession = Depends(get_db)):
    """Retrieve full session detail and scenario briefing."""
    data = curriculum_service.get_session_detail(db, session_id)
    if not data:
        raise HTTPException(status_code=404, detail="Session not found")
    return data
