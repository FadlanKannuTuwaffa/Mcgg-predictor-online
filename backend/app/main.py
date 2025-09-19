from fastapi import FastAPI, Depends, HTTPException, Header, BackgroundTasks
from sqlmodel import Session, select
from .db import init_db, engine
from .models import User, Match, PredictionStat
from .schemas import *
from .auth import hash_password, verify_password, create_access_token, decode_token
from .predictor import montecarlo_predict
from datetime import datetime, timedelta
import json, smtplib, os
from email.mime.text import MIMEText

app = FastAPI(title="MCGG-Xbot API")

# === STARTUP ===
@app.on_event("startup")
def on_start():
    init_db()

# === HELPER AUTH ===
def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, "Missing auth")
    token = authorization.split(" ")[-1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, "Invalid token")
    return payload

def send_email(to_email: str, subject: str, body: str):
    """Kirim email notifikasi expiry akun"""
    smtp_host = os.getenv("SMTP_HOST", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", 587))
    smtp_user = os.getenv("SMTP_USER", "")
    smtp_pass = os.getenv("SMTP_PASS", "")

    if not smtp_user or not smtp_pass:
        print("⚠️ SMTP not configured, skip email")
        return

    msg = MIMEText(body, "plain")
    msg["Subject"] = subject
    msg["From"] = smtp_user
    msg["To"] = to_email

    try:
        with smtplib.SMTP(smtp_host, smtp_port) as server:
            server.starttls()
            server.login(smtp_user, smtp_pass)
            server.send_message(msg)
            print(f"📧 Email sent to {to_email}")
    except Exception as e:
        print(f"Email error: {e}")

# === AUTH ROUTES ===
@app.post("/register", response_model=UserOut)
def register(data: UserCreate):
    with Session(engine) as s:
        exists = s.exec(select(User).where(User.username == data.username)).first()
        if exists:
            raise HTTPException(400, "Username exists")
        u = User(username=data.username, password_hash=hash_password(data.password), active=False)
        s.add(u)
        s.commit()
        s.refresh(u)
        return UserOut(id=u.id, username=u.username, active=u.active, expire_at=u.expire_at)

@app.post("/login")
def login(data: LoginIn, background: BackgroundTasks = None):
    with Session(engine) as s:
        u = s.exec(select(User).where(User.username == data.username)).first()
        if not u or not verify_password(data.password, u.password_hash):
            raise HTTPException(401, "Invalid credentials")
        if not u.active or (u.expire_at and u.expire_at < datetime.utcnow()):
            raise HTTPException(403, "Account not active or expired")

        # Kirim notifikasi jika expire < 3 hari
        if u.expire_at and (u.expire_at - datetime.utcnow()).days <= 3:
            background.add_task(
                send_email,
                u.username,  # Asumsikan username = email
                "⚠️ Akun MCGG-Xbot Hampir Expired",
                f"Halo {u.username}, akunmu akan expired pada {u.expire_at}. Silakan hubungi admin untuk perpanjangan."
            )

        token = create_access_token({"sub": u.username, "user_id": u.id})
        return {"access_token": token, "token_type": "bearer"}

@app.get("/me")
def me(auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        u = s.exec(select(User).where(User.username == auth["sub"])).first()
        if not u:
            raise HTTPException(404, "User not found")
        return {
            "username": u.username,
            "is_admin": u.is_admin,
            "active": u.active,
            "expire_at": u.expire_at,
        }

# === ADMIN ROUTES ===
@app.get("/admin/users")
def list_users(auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        admin = s.exec(select(User).where(User.username == auth["sub"])).first()
        if not admin or not admin.is_admin:
            raise HTTPException(403, "Not admin")
        return s.exec(select(User)).all()

@app.post("/admin/approve/{username}")
def admin_approve(username: str, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        u = s.exec(select(User).where(User.username == auth["sub"])).first()
        if not u or not u.is_admin:
            raise HTTPException(403, "Not admin")
        target = s.exec(select(User).where(User.username == username)).first()
        if not target:
            raise HTTPException(404, "Not found")
        target.active = True
        target.expire_at = datetime.utcnow() + timedelta(days=30)
        s.add(target)
        s.commit()
        return {"ok": True, "expire_at": target.expire_at}

@app.post("/admin/deactivate/{username}")
def admin_deactivate(username: str, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        u = s.exec(select(User).where(User.username == auth["sub"])).first()
        if not u or not u.is_admin:
            raise HTTPException(403, "Not admin")
        target = s.exec(select(User).where(User.username == username)).first()
        if not target:
            raise HTTPException(404, "Not found")
        target.active = False
        s.add(target)
        s.commit()
        return {"ok": True}

# === MATCH ROUTES ===
@app.post("/match/start")
def start_match(data: PlayerListIn, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == auth["sub"])).first()
        m = Match(user_id=user.id, rounds_data=json.dumps([]))
        s.add(m)
        s.commit()
        s.refresh(m)
        return {"match_id": m.id, "players": data.players}

@app.post("/match/predict")
def predict(payload: PlayerListIn, auth: dict = Depends(get_current_user)):
    players_list = payload.players
    if len(players_list) < 2:
        raise HTTPException(400, "Need players")
    top2 = montecarlo_predict(players_list[0], players_list, sims=1000)

    # Simpan statistik
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == auth["sub"])).first()
        for opp, prob in top2:
            stat = s.exec(
                select(PredictionStat).where(PredictionStat.user_id == user.id, PredictionStat.key == opp)
            ).first()
            if not stat:
                stat = PredictionStat(user_id=user.id, key=opp, count=0)
            stat.count += 1
            s.add(stat)
        s.commit()

    return {"predictions": top2}

@app.get("/match/stats")
def get_stats(auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == auth["sub"])).first()
        stats = s.exec(select(PredictionStat).where(PredictionStat.user_id == user.id)).all()
        return [{"opponent": st.key, "count": st.count} for st in stats]

@app.post("/match/round")
def round_update(data: RoundInput, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == auth["sub"])).first()
        m = s.exec(select(Match).where(Match.id == data.match_id, Match.user_id == user.id)).first()
        if not m:
            raise HTTPException(404, "match not found")
        rounds = json.loads(m.rounds_data or "[]")
        rounds.append({"round": data.round_name, "opponent": data.opponent, "ts": datetime.utcnow().isoformat()})
        m.rounds_data = json.dumps(rounds)
        s.add(m)
        s.commit()
        return {"ok": True, "rounds": rounds}

@app.post("/match/eliminate")
def mark_elim(data: EliminateIn, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == auth["sub"])).first()
        m = s.exec(select(Match).where(Match.id == data.match_id, Match.user_id == user.id)).first()
        if not m:
            raise HTTPException(404, "match not found")
        rounds = json.loads(m.rounds_data or "[]")
        rounds.append({"event": "eliminate", "player": data.eliminated, "ts": datetime.utcnow().isoformat()})
        m.rounds_data = json.dumps(rounds)
        s.add(m)
        s.commit()
        return {"ok": True}

@app.post("/match/finish")
def finish_match(match_id: int, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == auth["sub"])).first()
        m = s.exec(select(Match).where(Match.id == match_id, Match.user_id == user.id)).first()
        if not m:
            raise HTTPException(404, "match not found")
        m.finished = True
        rounds = json.loads(m.rounds_data or "[]")
        m.result_summary = f"rounds={len(rounds)}"
        s.add(m)
        s.commit()
        return {"ok": True, "summary": m.result_summary}

@app.get("/match/history")
def match_history(auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username == auth["sub"])).first()
        matches = s.exec(select(Match).where(Match.user_id == user.id)).all()
        return [{"id": m.id, "summary": m.result_summary, "created_at": m.created_at} for m in matches]
