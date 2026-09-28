from typing import Optional, Dict, Any, List
from pydantic import BaseModel, ConfigDict


class SettingsUpdate(BaseModel):
    stt_model: Optional[str] = None
    llm_model: Optional[str] = None
    tts_voice: Optional[str] = None
    tts_speed: Optional[str] = None
    input_mode: Optional[str] = None
    auto_play_audio: Optional[str] = None
    store_audio: Optional[str] = None


class SettingsResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    stt_model: str
    llm_model: str
    tts_voice: str
    tts_speed: str
    input_mode: str
    auto_play_audio: str
    store_audio: str
    available_devices: List[str] = ["cpu"]
    current_device: str = "cpu"
    is_cuda_available: bool = False


class ProgressSummaryResponse(BaseModel):
    total_sessions_completed: int
    total_speaking_time_minutes: float
    average_score: int
    best_score: int
    latest_score: int
    current_estimated_cefr: str
    streak_days: int
    score_trend: List[Dict[str, Any]]
    genre_progress: List[Dict[str, Any]]
