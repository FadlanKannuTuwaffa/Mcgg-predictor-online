import os
from sqlmodel import SQLModel, create_engine
from dotenv import load_dotenv

load_dotenv()

# Use Replit built-in PostgreSQL credentials directly
PGHOST = os.getenv("PGHOST")
PGUSER = os.getenv("PGUSER") 
PGPASSWORD = os.getenv("PGPASSWORD")
PGDATABASE = os.getenv("PGDATABASE")
PGPORT = os.getenv("PGPORT", "5432")

# Construct DATABASE_URL from individual components
if PGHOST and PGUSER and PGPASSWORD and PGDATABASE:
    DATABASE_URL = f"postgresql://{PGUSER}:{PGPASSWORD}@{PGHOST}:{PGPORT}/{PGDATABASE}"
else:
    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        raise ValueError("Database credentials are not configured properly.")

# SQLModel engine
engine = create_engine(DATABASE_URL, echo=False)

def init_db():
    """Initialize database - create all tables"""
    try:
        SQLModel.metadata.create_all(engine)
        print("Database tables created successfully")
    except Exception as e:
        print(f"Error creating database tables: {e}")
        raise e  # Fail fast if database is not accessible

def get_db():
    """Dependency to get database session"""
    from sqlmodel import Session
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()