from typing import List, Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import desc

from backend.app.database import get_db
from backend.app.models.attempt import SessionAttempt
from backend.app.models.evaluation import Evaluation
from backend.app.models.session import Session
from backend.app.models.genre import Genre
from backend.app.models.unit import Unit
from backend.app.schemas.settings import ProgressSummaryResponse

router = APIRouter(prefix="/progress", tags=["Progress"])


@router.get("/summary", response_model=ProgressSummaryResponse)
def get_progress_summary(db: DBSession = Depends(get_db)):
    """Retrieve aggregate progress metrics, speaking time, and historical score trend."""
    completed_attempts = (
        db.query(SessionAttempt)
        .filter(SessionAttempt.status == "COMPLETED")
        .order_by(SessionAttempt.started_at.asc())
        .all()
    )
    
    total_completed = len(completed_attempts)
    evals = db.query(Evaluation).order_by(Evaluation.created_at.asc()).all()
    
    total_speaking_sec = sum(e.total_speaking_time for e in evals)
    total_speaking_min = round(total_speaking_sec / 60.0, 1)
    
    scores = [e.overall_score for e in evals]
    avg_score = int(sum(scores) / max(1, len(scores))) if scores else 0
    best_score = max(scores) if scores else 0
    latest_score = scores[-1] if scores else 0
    current_cefr = evals[-1].estimated_cefr if evals else "A1"

    score_trend = []
    for idx, e in enumerate(evals):
        score_trend.append({
            "session_num": idx + 1,
            "overall": e.overall_score,
            "fluency": e.fluency,
            "accuracy": e.accuracy,
            "grammar": e.grammar,
            "vocabulary": e.vocabulary,
            "date": e.created_at.strftime("%b %d")
        })

    # Genre breakdown progress
    genres = db.query(Genre).all()
    genre_progress = []
    for g in genres:
        total_s = db.query(Session).filter(Session.genre_id == g.id).count()
        comp_s = (
            db.query(SessionAttempt.session_id)
            .join(Session, SessionAttempt.session_id == Session.id)
            .filter(Session.genre_id == g.id, SessionAttempt.status == "COMPLETED")
            .distinct()
            .count()
        )
        pct = int((comp_s / max(1, total_s)) * 100) if total_s > 0 else 0
        genre_progress.append({
            "id": g.id,
            "title": g.title,
            "total_sessions": total_s,
            "completed_sessions": comp_s,
            "percentage": pct
        })

    return {
        "total_sessions_completed": total_completed,
        "total_speaking_time_minutes": total_speaking_min,
        "average_score": avg_score,
        "best_score": best_score,
        "latest_score": latest_score,
        "current_estimated_cefr": current_cefr,
        "streak_days": min(total_completed, 7),
        "score_trend": score_trend,
        "genre_progress": genre_progress
    }


@router.get("/history")
def get_session_history(db: DBSession = Depends(get_db)):
    """Retrieve full history of all session attempts with evaluation snapshots."""
    attempts = (
        db.query(SessionAttempt)
        .order_by(desc(SessionAttempt.started_at))
        .all()
    )
    
    results = []
    for att in attempts:
        sess = att.session
        genre = sess.genre if sess else None
        unit = sess.unit if sess else None
        evaluation = att.evaluation

        results.append({
            "attempt_id": att.id,
            "session_id": att.session_id,
            "session_title": sess.title if sess else "Speaking Session",
            "genre_title": genre.title if genre else "General",
            "unit_title": unit.title if unit else "General",
            "difficulty": sess.difficulty if sess else "Intermediate",
            "status": att.status,
            "started_at": att.started_at.isoformat() if att.started_at else None,
            "duration_seconds": att.session_duration,
            "turn_count": att.turn_count,
            "overall_score": evaluation.overall_score if evaluation else None,
            "estimated_cefr": evaluation.estimated_cefr if evaluation else None,
            "has_evaluation": evaluation is not None
        })

    return results
