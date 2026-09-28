from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Float, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Evaluation(Base):
    __tablename__ = "evaluations"

    id = Column(Integer, primary_key=True, index=True)
    attempt_id = Column(Integer, ForeignKey("session_attempts.id", ondelete="CASCADE"), unique=True, nullable=False)
    
    overall_score = Column(Integer, default=0)
    fluency = Column(Integer, default=0)
    accuracy = Column(Integer, default=0)
    grammar = Column(Integer, default=0)
    vocabulary = Column(Integer, default=0)
    pronunciation_estimate = Column(Integer, default=0)
    comprehension = Column(Integer, default=0)
    sentence_formation = Column(Integer, default=0)
    naturalness = Column(Integer, default=0)
    conversation_relevance = Column(Integer, default=0)
    confidence_estimate = Column(Integer, default=0)
    
    estimated_cefr = Column(String(10), default="B1")
    cefr_reasoning = Column(Text, nullable=True)
    
    total_speaking_time = Column(Float, default=0.0)
    turn_count = Column(Integer, default=0)
    avg_response_words = Column(Float, default=0.0)
    
    filler_count = Column(Integer, default=0)
    filler_rate = Column(Float, default=0.0)
    most_used_filler = Column(String(50), nullable=True)
    filler_breakdown = Column(JSON, default=dict)
    repetition_analysis = Column(JSON, default=dict)
    
    strengths = Column(JSON, default=list)
    improvements = Column(JSON, default=list)
    naturalness_tips = Column(JSON, default=list)
    recommendations = Column(JSON, default=list)
    
    raw_analysis_json = Column(JSON, default=dict)
    created_at = Column(DateTime, default=datetime.utcnow)

    attempt = relationship("SessionAttempt", back_populates="evaluation")
    corrections = relationship("Correction", back_populates="evaluation", cascade="all, delete-orphan")
    vocabulary_items = relationship("VocabularyFeedback", back_populates="evaluation", cascade="all, delete-orphan")
