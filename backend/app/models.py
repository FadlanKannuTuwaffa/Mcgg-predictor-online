# backend/app/models.py
from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime

class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    username: str = Field(index=True, unique=True)
    password_hash: str
    is_admin: bool = False
    active: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    expire_at: Optional[datetime] = None
    email: Optional[str] = None

class Match(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    finished: bool = False
    rounds_data: Optional[str] = None
    result_summary: Optional[str] = None

class PredictionStat(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(index=True)
    key: str
    count: int = 0
    last_updated: Optional[datetime] = None
