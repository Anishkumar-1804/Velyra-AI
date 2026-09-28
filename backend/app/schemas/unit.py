from typing import Optional
from pydantic import BaseModel, ConfigDict


class UnitBase(BaseModel):
    genre_id: int
    slug: str
    title: str
    description: str
    order_index: int = 0


class UnitResponse(UnitBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    session_count: Optional[int] = 0
    completed_sessions: Optional[int] = 0
    progress_percentage: Optional[int] = 0
