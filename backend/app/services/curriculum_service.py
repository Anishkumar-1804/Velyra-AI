from typing import List, Dict, Any, Optional
from sqlalchemy.orm import Session as DBSession
from sqlalchemy import func

from backend.app.models.genre import Genre
from backend.app.models.unit import Unit
from backend.app.models.session import Session
from backend.app.models.attempt import SessionAttempt
from backend.app.models.evaluation import Evaluation


class CurriculumService:
    """
    Curriculum querying service with calculated completion and scoring metrics.
    """
    def get_all_genres(self, db: DBSession) -> List[Dict[str, Any]]:
        genres = db.query(Genre).order_by(Genre.order_index.asc()).all()
        result = []
        for g in genres:
            unit_count = len(g.units)
            all_sessions = db.query(Session).filter(Session.genre_id == g.id).all()
            session_count = len(all_sessions)
            
            # Count how many sessions in this genre have completed attempts
            completed_count = (
                db.query(SessionAttempt.session_id)
                .join(Session, SessionAttempt.session_id == Session.id)
                .filter(Session.genre_id == g.id, SessionAttempt.status == "COMPLETED")
                .distinct()
                .count()
            )
            progress = int((completed_count / max(1, session_count)) * 100) if session_count > 0 else 0

            result.append({
                "id": g.id,
                "slug": g.slug,
                "title": g.title,
                "description": g.description,
                "icon": g.icon,
                "order_index": g.order_index,
                "unit_count": unit_count,
                "session_count": session_count,
                "completed_sessions": completed_count,
                "progress_percentage": progress
            })
        return result

    def get_genre_by_id(self, db: DBSession, genre_id: int) -> Optional[Dict[str, Any]]:
        g = db.query(Genre).filter(Genre.id == genre_id).first()
        if not g:
            return None
        
        units_data = []
        for u in g.units:
            sessions = db.query(Session).filter(Session.unit_id == u.id).order_by(Session.order_index.asc()).all()
            session_count = len(sessions)
            completed_count = (
                db.query(SessionAttempt.session_id)
                .join(Session, SessionAttempt.session_id == Session.id)
                .filter(Session.unit_id == u.id, SessionAttempt.status == "COMPLETED")
                .distinct()
                .count()
            )
            progress = int((completed_count / max(1, session_count)) * 100) if session_count > 0 else 0

            units_data.append({
                "id": u.id,
                "genre_id": u.genre_id,
                "slug": u.slug,
                "title": u.title,
                "description": u.description,
                "order_index": u.order_index,
                "session_count": session_count,
                "completed_sessions": completed_count,
                "progress_percentage": progress
            })

        return {
            "id": g.id,
            "slug": g.slug,
            "title": g.title,
            "description": g.description,
            "icon": g.icon,
            "order_index": g.order_index,
            "units": units_data
        }

    def get_unit_by_id(self, db: DBSession, unit_id: int) -> Optional[Dict[str, Any]]:
        u = db.query(Unit).filter(Unit.id == unit_id).first()
        if not u:
            return None

        sessions = db.query(Session).filter(Session.unit_id == u.id).order_by(Session.order_index.asc()).all()
        sessions_data = []

        for s in sessions:
            attempts = db.query(SessionAttempt).filter(SessionAttempt.session_id == s.id).all()
            completed_attempts = [a for a in attempts if a.status == "COMPLETED"]
            
            best_score = None
            if completed_attempts:
                evals = db.query(Evaluation).filter(Evaluation.attempt_id.in_([a.id for a in completed_attempts])).all()
                if evals:
                    best_score = max(e.overall_score for e in evals)

            sessions_data.append({
                "id": s.id,
                "unit_id": s.unit_id,
                "genre_id": s.genre_id,
                "slug": s.slug,
                "title": s.title,
                "description": s.description,
                "difficulty": s.difficulty,
                "cefr_level": s.cefr_level,
                "estimated_duration": s.estimated_duration,
                "target_turns": s.target_turns,
                "order_index": s.order_index,
                "is_completed": len(completed_attempts) > 0,
                "best_score": best_score,
                "attempt_count": len(attempts)
            })

        return {
            "id": u.id,
            "genre_id": u.genre_id,
            "genre_title": u.genre.title if u.genre else "",
            "slug": u.slug,
            "title": u.title,
            "description": u.description,
            "order_index": u.order_index,
            "sessions": sessions_data
        }

    def get_session_detail(self, db: DBSession, session_id: int) -> Optional[Dict[str, Any]]:
        s = db.query(Session).filter(Session.id == session_id).first()
        if not s:
            return None

        attempts = db.query(SessionAttempt).filter(SessionAttempt.session_id == s.id).all()
        completed_attempts = [a for a in attempts if a.status == "COMPLETED"]
        
        best_score = None
        if completed_attempts:
            evals = db.query(Evaluation).filter(Evaluation.attempt_id.in_([a.id for a in completed_attempts])).all()
            if evals:
                best_score = max(e.overall_score for e in evals)

        return {
            "id": s.id,
            "unit_id": s.unit_id,
            "genre_id": s.genre_id,
            "slug": s.slug,
            "title": s.title,
            "description": s.description,
            "difficulty": s.difficulty,
            "cefr_level": s.cefr_level,
            "scenario": s.scenario,
            "ai_role": s.ai_role,
            "user_role": s.user_role,
            "learning_objectives": s.learning_objectives or [],
            "allowed_topics": s.allowed_topics or [],
            "forbidden_topics": s.forbidden_topics or [],
            "conversation_stages": s.conversation_stages or [],
            "opening_message": s.opening_message,
            "completion_conditions": s.completion_conditions or [],
            "suggested_vocabulary": s.suggested_vocabulary or [],
            "estimated_duration": s.estimated_duration,
            "target_turns": s.target_turns,
            "order_index": s.order_index,
            "is_completed": len(completed_attempts) > 0,
            "best_score": best_score,
            "attempt_count": len(attempts),
            "genre_title": s.genre.title if s.genre else "",
            "unit_title": s.unit.title if s.unit else ""
        }


curriculum_service = CurriculumService()
