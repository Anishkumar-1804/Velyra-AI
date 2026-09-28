from datetime import datetime
from typing import List, Optional
from pydantic import BaseModel, ConfigDict


class TurnCreate(BaseModel):
    attempt_id: int
    transcript: str
    speaker: str = "user"
    audio_duration: float = 0.0
    confidence: Optional[float] = None
    filler_count: int = 0
    detected_fillers: List[str] = []
    pause_count: int = 0


class TurnResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    attempt_id: int
    turn_index: int
    speaker: str
    transcript: str
    audio_url: Optional[str] = None
    audio_duration: float
    confidence: Optional[float] = None
    filler_count: int = 0
    detected_fillers: List[str] = []
    pause_count: int = 0
    created_at: datetime


class StartSessionRequest(BaseModel):
    session_id: int


class StartSessionResponse(BaseModel):
    attempt_id: int
    session_id: int
    status: str
    opening_message: str
    ai_role: str
    user_role: str
    scenario: str
    target_turns: int
    current_stage: int
    total_stages: int
    audio_url: Optional[str] = None


class UserSpeechTurnRequest(BaseModel):
    attempt_id: int
    transcript: Optional[str] = None


class UserTurnResponse(BaseModel):
    user_turn: TurnResponse
    ai_turn: TurnResponse
    current_stage: int
    total_stages: int
    turn_count: int
    is_completed: bool
    session_status: str
    session_guard_passed: bool = True
    ai_audio_url: Optional[str] = None
