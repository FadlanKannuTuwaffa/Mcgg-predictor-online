# backend/app/db.py
from sqlmodel import SQLModel, create_engine, Session
import os

# Tentukan path DB yang aman
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
db_path = os.path.join(BASE_DIR, "mcgg.db")

# Utamakan DATABASE_URL dari environment, fallback ke SQLite lokal
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{db_path}")

engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as s:
        yield s
