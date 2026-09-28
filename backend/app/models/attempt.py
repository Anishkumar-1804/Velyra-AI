from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float
from sqlalchemy.orm import relationship
from backend.app.database import Base


class SessionAttempt(Base):
    __tablename__ = "session_attempts"

    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(Integer, ForeignKey("sessions.id", ondelete="CASCADE"), nullable=False)
    status = Column(String(50), default="ACTIVE")  # ACTIVE, PAUSED, COMPLETED, CANCELLED
    current_stage = Column(Integer, default=0)
    turn_count = Column(Integer, default=0)
    user_turn_count = Column(Integer, default=0)
    ai_turn_count = Column(Integer, default=0)
    
    total_speaking_duration = Column(Float, default=0.0)  # total seconds user spoke
    session_duration = Column(Float, default=0.0)  # total session seconds
    
    last_user_turn = Column(Text, nullable=True)
    last_ai_turn = Column(Text, nullable=True)
    
    started_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    session = relationship("Session", back_populates="attempts")
    turns = relationship("ConversationTurn", back_populates="attempt", cascade="all, delete-orphan", order_by="ConversationTurn.turn_index")
    evaluation = relationship("Evaluation", back_populates="attempt", uselist=False, cascade="all, delete-orphan")
