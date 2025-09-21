from pydantic import BaseModel
from typing import List, Optional

class UserCreate(BaseModel):
    username: str
    password: str

class UserOut(BaseModel):
    id: int
    username: str
    active: bool
    expire_at: Optional[str]

class LoginIn(BaseModel):
    username: str
    password: str

class PlayerListIn(BaseModel):
    players: List[str]

class RoundInput(BaseModel):
    match_id: int
    round_name: str
    opponent: str

class EliminateIn(BaseModel):
    match_id: int
    eliminated: str