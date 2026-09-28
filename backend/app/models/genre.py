from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.orm import relationship
from backend.app.database import Base


class Genre(Base):
    __tablename__ = "genres"

    id = Column(Integer, primary_key=True, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=False)
    icon = Column(String(100), nullable=True)
    order_index = Column(Integer, default=0)

    units = relationship("Unit", back_populates="genre", cascade="all, delete-orphan", order_by="Unit.order_index")
