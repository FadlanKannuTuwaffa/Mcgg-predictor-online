# backend/app/main.py
from fastapi import FastAPI, Depends, HTTPException, Header, BackgroundTasks
from sqlmodel import Session, select
from .db import init_db, engine
from .models import User, Match, PredictionStat
from .schemas import *
from .auth import hash_password, verify_password, create_access_token, decode_token, get_current_user
from .predictor import montecarlo_predict
from datetime import datetime, timedelta
import json, os, smtplib, ssl
from email.message import EmailMessage

app = FastAPI(title="MCGG-Xbot API")

@app.on_event("startup")
def on_start():
    init_db()

def send_email(to_address: str, subject: str, body: str):
    host = os.getenv("SMTP_HOST")
    port = int(os.getenv("SMTP_PORT", "587"))
    user = os.getenv("SMTP_USER")
    password = os.getenv("SMTP_PASS")
    sender = os.getenv("SMTP_SENDER", user)
    if not host or not user or not password:
        # email not configured
        return False
    msg = EmailMessage()
    msg["From"] = sender
    msg["To"] = to_address
    msg["Subject"] = subject
    msg.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP(host, port) as server:
        server.starttls(context=context)
        server.login(user, password)
        server.send_message(msg)
    return True

@app.post('/register', response_model=UserOut)
def register(data: UserCreate):
    with Session(engine) as s:
        if s.exec(select(User).where(User.username==data.username)).first():
            raise HTTPException(400, 'Username exists')
        u = User(username=data.username, password_hash=hash_password(data.password), active=False)
        s.add(u); s.commit(); s.refresh(u)
        return UserOut(id=u.id, username=u.username, active=u.active, expire_at=u.expire_at)

@app.post('/login')
def login(data: LoginIn):
    with Session(engine) as s:
        u = s.exec(select(User).where(User.username==data.username)).first()
        if not u or not verify_password(data.password, u.password_hash):
            raise HTTPException(401, 'Invalid credentials')
        if not u.active or (u.expire_at and u.expire_at < datetime.utcnow()):
            raise HTTPException(403, 'Account not active or expired')
        token = create_access_token({'sub': u.username, 'user_id': u.id})
        return {'access_token': token, 'token_type': 'bearer'}

@app.get('/me')
def me(auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        u = s.exec(select(User).where(User.username==auth['sub'])).first()
        if not u:
            raise HTTPException(404, 'Not found')
        return {"username": u.username, "is_admin": u.is_admin, "active": u.active, "expire_at": u.expire_at}

@app.post('/admin/approve/{username}')
def admin_approve(username: str, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        admin = s.exec(select(User).where(User.username==auth['sub'])).first()
        if not admin or not admin.is_admin:
            raise HTTPException(403, 'Not admin')
        target = s.exec(select(User).where(User.username==username)).first()
        if not target:
            raise HTTPException(404, 'Not found')
        target.active = True
        target.expire_at = datetime.utcnow() + timedelta(days=30)
        s.add(target); s.commit()
        # optionally email
        if target.email:
            send_email(target.email, "Akun Diaktifkan", f"Akun {target.username} diaktifkan sampai {target.expire_at}.")
        return {'ok': True}

@app.get('/admin/users')
def admin_users(auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        admin = s.exec(select(User).where(User.username==auth['sub'])).first()
        if not admin or not admin.is_admin:
            raise HTTPException(403, 'Not admin')
        users = s.exec(select(User)).all()
        out = [{"username": u.username, "active": u.active, "expire_at": u.expire_at} for u in users]
        return out

@app.post('/match/start')
def start_match(data: PlayerListIn, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username==auth['sub'])).first()
        m = Match(user_id=user.id, rounds_data=json.dumps([]))
        s.add(m); s.commit(); s.refresh(m)
        return {'match_id': m.id, 'players': data.players}

@app.post('/match/predict')
def predict(payload: PlayerListIn, auth: dict = Depends(get_current_user)):
    players_list = payload.players
    if len(players_list) < 2:
        raise HTTPException(400, 'Need players')
    top2 = montecarlo_predict(players_list[0], players_list, sims=500)
    return {'predictions': top2}

@app.post('/match/round')
def round_update(data: RoundInput, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username==auth['sub'])).first()
        m = s.exec(select(Match).where(Match.id==data.match_id, Match.user_id==user.id)).first()
        if not m: raise HTTPException(404, 'match not found')
        rounds = json.loads(m.rounds_data or '[]')
        rounds.append({'round': data.round_name, 'opponent': data.opponent, 'ts': datetime.utcnow().isoformat()})
        m.rounds_data = json.dumps(rounds)
        s.add(m); s.commit()
        return {'ok': True, 'rounds': rounds}

@app.post('/match/eliminate')
def mark_elim(data: EliminateIn, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username==auth['sub'])).first()
        m = s.exec(select(Match).where(Match.id==data.match_id, Match.user_id==user.id)).first()
        if not m: raise HTTPException(404, 'match not found')
        rounds = json.loads(m.rounds_data or '[]')
        rounds.append({'event': 'eliminate', 'player': data.eliminated, 'ts': datetime.utcnow().isoformat()})
        m.rounds_data = json.dumps(rounds)
        s.add(m); s.commit()
        return {'ok': True}

@app.post('/match/finish')
def finish_match(match_id: int, background_tasks: BackgroundTasks, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username==auth['sub'])).first()
        m = s.exec(select(Match).where(Match.id==match_id, Match.user_id==user.id)).first()
        if not m: raise HTTPException(404, 'match not found')
        m.finished = True
        rounds = json.loads(m.rounds_data or '[]')
        m.result_summary = f'rounds={len(rounds)}'
        s.add(m); s.commit()

        # Update prediction stats simple example
        # For demonstration, increment stat for first predicted opponent if present
        try:
            # naive: read last predicted opponent from rounds
            if rounds:
                # find last opponent entries
                opps = [r.get("opponent") for r in rounds if 'opponent' in r]
                if opps:
                    key = opps[-1]
                    stat = s.exec(select(PredictionStat).where(PredictionStat.user_id==user.id, PredictionStat.key==key)).first()
                    if stat:
                        stat.count += 1
                        stat.last_updated = datetime.utcnow()
                        s.add(stat)
                    else:
                        s.add(PredictionStat(user_id=user.id, key=key, count=1, last_updated=datetime.utcnow()))
                    s.commit()
        except Exception:
            pass

        return {'ok': True}

@app.get('/stats')
def get_stats(auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username==auth['sub'])).first()
        stats = s.exec(select(PredictionStat).where(PredictionStat.user_id==user.id)).all()
        return [{"key": st.key, "count": st.count} for st in stats]

# Admin: run daily check to email users near expiry (optional endpoint)
@app.post("/admin/check-expiry")
def check_expiry(background_tasks: BackgroundTasks, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        admin = s.exec(select(User).where(User.username==auth['sub'])).first()
        if not admin or not admin.is_admin:
            raise HTTPException(403, "Not admin")
        now = datetime.utcnow()
        users = s.exec(select(User).where(User.active==True)).all()
        for u in users:
            if u.expire_at and (u.expire_at - now).days <= 3:
                if u.email:
                    background_tasks.add_task(send_email, u.email, "Akun segera kadaluwarsa", f"Akun Anda akan kadaluwarsa pada {u.expire_at}")
    return {"ok": True}
