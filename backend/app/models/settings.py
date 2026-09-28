from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, DateTime, JSON
from backend.app.database import Base


class UserSettings(Base):
    __tablename__ = "user_settings"

    id = Column(Integer, primary_key=True, default=1)
    stt_model = Column(String(50), default="base.en")
    llm_model = Column(String(100), default="Qwen/Qwen2.5-0.5B-Instruct")
    tts_voice = Column(String(100), default="en-IN-NeerjaNeural")
    tts_speed = Column(String(20), default="1.0")
    input_mode = Column(String(50), default="auto_vad")  # 'auto_vad' or 'push_to_talk'
    auto_play_audio = Column(String(10), default="true")
    store_audio = Column(String(10), default="false")
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class ProgressSnapshot(Base):
    __tablename__ = "progress_snapshots"

    id = Column(Integer, primary_key=True, index=True)
    timestamp = Column(DateTime, default=datetime.utcnow)
    total_speaking_time = Column(Integer, default=0)  # total seconds
    total_sessions_completed = Column(Integer, default=0)
    current_estimated_cefr = Column(String(10), default="A1")
    avg_score = Column(Integer, default=0)
    fluency_avg = Column(Integer, default=0)
    grammar_avg = Column(Integer, default=0)
    vocab_avg = Column(Integer, default=0)
    metadata_json = Column(JSON, default=dict)
