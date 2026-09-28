from sqlalchemy import Column, Integer, String, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Session(Base):
    __tablename__ = "sessions"

    id = Column(Integer, primary_key=True, index=True)
    unit_id = Column(Integer, ForeignKey("units.id", ondelete="CASCADE"), nullable=False)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), nullable=False)
    slug = Column(String(150), index=True, nullable=False)
    title = Column(String(250), nullable=False)
    description = Column(Text, nullable=False)
    difficulty = Column(String(50), default="Intermediate")  # Beginner, Elementary, Intermediate, Upper Intermediate, Advanced
    cefr_level = Column(String(10), default="B1")  # A1, A2, B1, B2, C1
    
    scenario = Column(Text, nullable=False)
    ai_role = Column(String(150), nullable=False)
    user_role = Column(String(150), nullable=False)
    
    learning_objectives = Column(JSON, nullable=False, default=list)
    allowed_topics = Column(JSON, nullable=False, default=list)
    forbidden_topics = Column(JSON, nullable=False, default=list)
    conversation_stages = Column(JSON, nullable=False, default=list)
    
    opening_message = Column(Text, nullable=False)
    completion_conditions = Column(JSON, nullable=False, default=list)
    suggested_vocabulary = Column(JSON, nullable=False, default=list)
    
    estimated_duration = Column(Integer, default=5)  # in minutes
    target_turns = Column(Integer, default=6)
    order_index = Column(Integer, default=0)

    unit = relationship("Unit", back_populates="sessions")
    genre = relationship("Genre")
    attempts = relationship("SessionAttempt", back_populates="session", cascade="all, delete-orphan", order_by="desc(SessionAttempt.started_at)")
