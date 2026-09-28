from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base


class ConversationTurn(Base):
    __tablename__ = "conversation_turns"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("session_attempts.id", ondelete="CASCADE"), nullable=False)
    turn_index = Column(Integer, nullable=False)
    speaker = Column(String(10), nullable=False)  # 'user' or 'ai'
    transcript = Column(Text, nullable=False)
    
    audio_url = Column(String(500), nullable=True)
    audio_duration = Column(Float, default=0.0)
    
    # Measurements from STT/VAD
    confidence = Column(Float, nullable=True)
    filler_count = Column(Integer, default=0)
    detected_fillers = Column(JSON, default=list)
    pause_count = Column(Integer, default=0)
    
    created_at = Column(DateTime, default=datetime.utcnow)

    attempt = relationship("SessionAttempt", back_populates="turns")
