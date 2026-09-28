from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session as DBSession

from backend.app.database import get_db
from backend.app.schemas.evaluation import EvaluationResponse
from backend.app.services.evaluation_service import evaluation_service
from backend.app.models.evaluation import Evaluation

router = APIRouter(prefix="/evaluation", tags=["Evaluation"])


@router.post("/attempt/{attempt_id}", response_model=EvaluationResponse)
def evaluate_session_attempt(attempt_id: int, db: DBSession = Depends(get_db)):
    """
    Run evidence-based evaluation on the finished attempt transcript.
    Generates scores, CEFR estimate, grammatical corrections, and vocabulary feedback.
    """
    try:
        eval_record = evaluation_service.evaluate_attempt(db, attempt_id)
        return eval_record
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/attempt/{attempt_id}", response_model=EvaluationResponse)
def get_attempt_evaluation(attempt_id: int, db: DBSession = Depends(get_db)):
    """Get the evaluated report for a specific attempt."""
    eval_record = db.query(Evaluation).filter(Evaluation.attempt_id == attempt_id).first()
    if not eval_record:
        # If not evaluated yet, trigger evaluation
        eval_record = evaluation_service.evaluate_attempt(db, attempt_id)
    return eval_record
