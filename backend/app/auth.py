# backend/app/auth.py
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
import os
import secrets

pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")

# Pakai secret dari environment; kalau tidak ada, generate random sementara
SECRET = os.getenv("JWT_SECRET")
if not SECRET:
    # ⚠️ Peringatan: random secret ini akan berubah setiap restart
    # Jadi hanya cocok untuk development, bukan production
    SECRET = secrets.token_hex(32)

ALGORITHM = "HS256"
ACCESS_EXPIRE_MINUTES = 60 * 24 * 7  # 7 hari

def hash_password(pw: str):
    return pwd_ctx.hash(pw)

def verify_password(pw: str, hashed: str):
    return pwd_ctx.verify(pw, hashed)

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET, algorithm=ALGORITHM)

def decode_token(token: str):
    try:
        payload = jwt.decode(token, SECRET, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None
