from typing import List, Dict, Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from backend.app.database import get_db
from backend.app.schemas.genre import GenreResponse
from backend.app.services.curriculum_service import curriculum_service

router = APIRouter(prefix="/genres", tags=["Genres"])


@router.get("", response_model=List[GenreResponse])
def list_genres(db: DBSession = Depends(get_db)):
    """Retrieve all speaking genres with user progress."""
    return curriculum_service.get_all_genres(db)


@router.get("/{genre_id}")
def get_genre(genre_id: int, db: DBSession = Depends(get_db)):
    """Retrieve a specific genre with its units."""
    data = curriculum_service.get_genre_by_id(db, genre_id)
    if not data:
        raise HTTPException(status_code=404, detail="Genre not found")
    return data
