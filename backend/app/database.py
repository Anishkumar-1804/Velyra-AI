import os
import logging
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from backend.app.config import settings

logger = logging.getLogger("angiyam.database")

engine = create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in settings.DATABASE_URL else {},
    echo=False
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

_db_initialized = False


def ensure_db_ready():
    """Ensure database schema is created and curriculum seeded (crucial for serverless environments)."""
    global _db_initialized
    if not _db_initialized:
        try:
            from backend.app import models  # register models
            Base.metadata.create_all(bind=engine)
            from backend.app.seed.curriculum import seed_curriculum
            db = SessionLocal()
            try:
                seed_curriculum(db)
            finally:
                db.close()
            _db_initialized = True
            logger.info("[Database] Auto-initialized schema and curriculum seed successfully.")
        except Exception as e:
            logger.error(f"[Database] Error in ensure_db_ready: {e}")


def get_db():
    ensure_db_ready()
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
