from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class SessionBase(BaseModel):
    unit_id: int
    genre_id: int
    slug: str
    title: str
    description: str
    difficulty: str
    cefr_level: str
    
    scenario: str
    ai_role: str
    user_role: str
    
    learning_objectives: List[str]
    allowed_topics: List[str]
    forbidden_topics: List[str]
    conversation_stages: List[str]
    
    opening_message: str
    completion_conditions: List[str]
    suggested_vocabulary: List[str] = []
    
    estimated_duration: int = 5
    target_turns: int = 6
    order_index: int = 0


class SessionSummary(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    unit_id: int
    genre_id: int
    slug: str
    title: str
    description: str
    difficulty: str
    cefr_level: str
    estimated_duration: int
    target_turns: int
    order_index: int
    is_completed: bool = False
    best_score: Optional[int] = None
    attempt_count: int = 0


class SessionDetail(SessionBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    is_completed: bool = False
    best_score: Optional[int] = None
    attempt_count: int = 0
    genre_title: Optional[str] = None
    unit_title: Optional[str] = None
