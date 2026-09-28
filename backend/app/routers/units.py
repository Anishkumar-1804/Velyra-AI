from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from backend.app.database import get_db
from backend.app.services.curriculum_service import curriculum_service

router = APIRouter(prefix="/units", tags=["Units"])


@router.get("/{unit_id}")
def get_unit(unit_id: int, db: DBSession = Depends(get_db)):
    """Retrieve unit details and its sessions."""
    data = curriculum_service.get_unit_by_id(db, unit_id)
    if not data:
        raise HTTPException(status_code=404, detail="Unit not found")
    return data
