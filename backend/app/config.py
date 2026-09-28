import os
from pathlib import Path
from pydantic_settings import BaseSettings
from pydantic import ConfigDict

BASE_DIR = Path(__file__).resolve().parent.parent.parent
is_serverless = os.environ.get("VERCEL") or os.environ.get("AWS_LAMBDA_FUNCTION_NAME") or not os.access(BASE_DIR, os.W_OK)
if is_serverless:
    DATA_DIR = Path("/tmp/data")
else:
    DATA_DIR = BASE_DIR / "data"

AUDIO_DIR = DATA_DIR / "audio"
MODELS_DIR = DATA_DIR / "models"
DB_PATH = DATA_DIR / "velyra.db" if not (DATA_DIR / "angiyam.db").exists() else (DATA_DIR / "angiyam.db")

# Ensure data directories exist
AUDIO_DIR.mkdir(parents=True, exist_ok=True)
MODELS_DIR.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    model_config = ConfigDict(env_file=".env", extra="ignore")

    APP_NAME: str = "Velyra.ai"
    APP_VERSION: str = "1.0.0"
    TAGLINE: str = "Speak English. Naturally."
    
    # Environment
    ENV: str = "development"
    DEBUG: bool = True
    DEV_AUDIO_MODE: bool = False  # Allows audio file uploads or synthetic fallbacks for testing
    
    # Database
    DATABASE_URL: str = f"sqlite:///{DB_PATH.as_posix()}"
    
    # Directory paths exposed on settings object
    BASE_DIR_PATH: Path = BASE_DIR
    DATA_DIR_PATH: Path = DATA_DIR
    AUDIO_DIR_PATH: Path = AUDIO_DIR
    MODELS_DIR_PATH: Path = MODELS_DIR
    
    # Device / Hardware detection
    DEVICE: str = "auto"  # 'auto', 'cuda', 'cpu'
    COMPUTE_TYPE: str = "auto"  # 'auto', 'int8', 'float16', 'float32'
    
    # Models Configuration
    STT_MODEL: str = "base.en"  # faster-whisper model: tiny.en, base.en, small.en
    LLM_MODEL: str = "Qwen/Qwen2.5-0.5B-Instruct"  # Local lightweight conversational LLM
    TTS_VOICE: str = "en-IN-NeerjaNeural"  # Natural Indian English Voice (female) or en-IN-PrabhatNeural (male)
    TTS_FALLBACK_VOICE: str = "en-IN"
    TTS_SPEED: float = 1.0  # 0.75x, 1.0x, 1.25x, 1.5x
    
    # Audio & Session Limits
    MAX_RECORDING_DURATION_SEC: int = 120
    MIN_RECORDING_DURATION_SEC: float = 0.5
    SILENCE_THRESHOLD_MS: int = 1200
    AUTO_PLAY_TTS: bool = True
    STORE_AUDIO_LOCALLY: bool = False
    
    # Session Guard
    MAX_GUARD_REGENERATIONS: int = 2

    @property
    def AUDIO_DIR(self) -> Path:
        return AUDIO_DIR

    @property
    def MODELS_DIR(self) -> Path:
        return MODELS_DIR


settings = Settings()
