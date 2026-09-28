from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Correction(Base):
    __tablename__ = "corrections"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id", ondelete="CASCADE"), nullable=False)
    
    user_said = Column(Text, nullable=False)
    better_version = Column(Text, nullable=False)
    issue = Column(String(200), nullable=False)
    explanation = Column(Text, nullable=False)
    category = Column(String(100), default="Grammar")  # Grammar, Tense, Preposition, Article, Word Choice, Naturalness

    evaluation = relationship("Evaluation", back_populates="corrections")


class VocabularyFeedback(Base):
    __tablename__ = "vocabulary_feedback"

    id = Column(Integer, primary_key=True, index=True)
    evaluation_id = Column(Integer, ForeignKey("evaluations.id", ondelete="CASCADE"), nullable=False)
    
    word_used = Column(String(200), nullable=False)
    better_alternative = Column(String(200), nullable=False)
    reason = Column(Text, nullable=False)
    example = Column(Text, nullable=False)

    evaluation = relationship("Evaluation", back_populates="vocabulary_items")
