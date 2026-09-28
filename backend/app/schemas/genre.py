from typing import Optional
from pydantic import BaseModel, ConfigDict


class GenreBase(BaseModel):
    slug: str
    title: str
    description: str
    icon: Optional[str] = None
    order_index: int = 0


class GenreResponse(GenreBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    unit_count: Optional[int] = 0
    session_count: Optional[int] = 0
    completed_sessions: Optional[int] = 0
    progress_percentage: Optional[int] = 0
