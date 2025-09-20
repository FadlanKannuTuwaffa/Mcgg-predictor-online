# backend/app/db.py
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

DATABASE_URL = os.getenv("postgresql://postgres:[fadlankannutuwaffa]@db.yomyntfbcoomgijcspfk.supabase.co:5432/postgres")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL is not set. Please configure it in Render environment variables.")

# SQLAlchemy setup
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
