"""
Standalone database creation and curriculum seeding script for Angiyam.ai
"""
import sys
from pathlib import Path

# Add project root to sys.path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from backend.app.database import engine, Base, SessionLocal
from backend.app.models import *  # register all models
from backend.app.seed.curriculum import seed_curriculum


def init_and_seed():
    print("[Database] Creating SQLite database tables if not present...")
    Base.metadata.create_all(bind=engine)
    print("[Database] Tables created successfully.")
    
    db = SessionLocal()
    try:
        seed_curriculum(db)
    finally:
        db.close()
    print("[Success] Angiyam.ai database ready!")


if __name__ == "__main__":
    init_and_seed()
