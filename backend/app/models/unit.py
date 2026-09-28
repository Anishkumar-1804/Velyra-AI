from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Unit(Base):
    __tablename__ = "units"

    id = Column(Integer, primary_key=True, index=True)
    genre_id = Column(Integer, ForeignKey("genres.id", ondelete="CASCADE"), nullable=False)
    slug = Column(String(100), index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    order_index = Column(Integer, default=0)

    genre = relationship("Genre", back_populates="units")
    sessions = relationship("Session", back_populates="unit", cascade="all, delete-orphan", order_by="Session.order_index")
