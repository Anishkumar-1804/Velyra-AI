import os
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse

from backend.app.config import settings
from backend.app.database import engine, Base, SessionLocal
from backend.app.models import *  # register models
from backend.app.seed.curriculum import seed_curriculum
from backend.app.routers import (
    genres,
    units,
    sessions,
    conversation,
    evaluation,
    progress,
    settings as settings_router
)

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s"
)
logger = logging.getLogger("velyra")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup: Ensure database tables exist and seed curriculum idempotently
    logger.info("Initializing Velyra.ai database tables...")
    Base.metadata.create_all(bind=engine)
    
    db = SessionLocal()
    try:
        seed_curriculum(db)
    except Exception as e:
        logger.error(f"Error during curriculum seeding: {e}")
    finally:
        db.close()
        
    # Pre-warm conversational LLM and STT to eliminate any user turn latency
    try:
        from backend.app.services.llm_service import llm_service
        from backend.app.services.stt_service import stt_service
        llm_service.warmup()
        stt_service.warmup()
    except Exception as e:
        logger.warning(f"Notice during model warmup: {e}")

    logger.info("Velyra.ai backend initialized and ready.")
    yield
    # Shutdown
    logger.info("Shutting down Velyra.ai backend.")


app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="Velyra.ai — Speak English. Naturally. Local-first voice AI English practice platform.",
    lifespan=lifespan
)

# Enable CORS for local React/Vite development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve generated TTS and audio files
tts_cache_dir = settings.AUDIO_DIR / "tts_cache"
tts_cache_dir.mkdir(parents=True, exist_ok=True)


@app.get("/api/audio/file/{filename}")
def serve_audio_file(filename: str):
    """Serve cached TTS audio file."""
    file_path = tts_cache_dir / filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="Audio file not found")
    media_type = "audio/mpeg" if filename.endswith(".mp3") else "audio/wav"
    return FileResponse(path=file_path, media_type=media_type)


# Mount REST Routers
app.include_router(genres.router, prefix="/api")
app.include_router(units.router, prefix="/api")
app.include_router(sessions.router, prefix="/api")
app.include_router(conversation.router, prefix="/api")
app.include_router(evaluation.router, prefix="/api")
app.include_router(progress.router, prefix="/api")
app.include_router(settings_router.router, prefix="/api")


@app.get("/api/health")
def health_check():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "tagline": settings.TAGLINE
    }
