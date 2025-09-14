from fastapi import FastAPI, Depends, HTTPException, Header
from sqlmodel import Session, select
from .db import init_db, engine
from .models import User, Match
from .schemas import *
from .auth import hash_password, verify_password, create_access_token, decode_token
from .predictor import montecarlo_predict
from datetime import datetime
import json

app = FastAPI(title='MCGG-Xbot API')

@app.on_event('startup')
def on_start():
    init_db()

def get_current_user(authorization: str = Header(None)):
    if not authorization:
        raise HTTPException(401, 'Missing auth')
    token = authorization.split(' ')[-1]
    payload = decode_token(token)
    if not payload:
        raise HTTPException(401, 'Invalid token')
    return payload

@app.post('/register', response_model=UserOut)
def register(data: UserCreate):
    with Session(engine) as s:
        exists = s.exec(select(User).where(User.username==data.username)).first()
        if exists:
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
        return {'access_token': token, 'token_type':'bearer'}

@app.post('/admin/approve/{username}')
def admin_approve(username: str, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        u = s.exec(select(User).where(User.username==auth['sub'])).first()
        if not u or not u.is_admin:
            raise HTTPException(403, 'Not admin')
        target = s.exec(select(User).where(User.username==username)).first()
        if not target:
            raise HTTPException(404, 'Not found')
        from datetime import timedelta
        target.active = True
        target.expire_at = datetime.utcnow() + timedelta(days=30)
        s.add(target); s.commit()
        return {'ok': True}

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
def finish_match(match_id: int, auth: dict = Depends(get_current_user)):
    with Session(engine) as s:
        user = s.exec(select(User).where(User.username==auth['sub'])).first()
        m = s.exec(select(Match).where(Match.id==match_id, Match.user_id==user.id)).first()
        if not m: raise HTTPException(404, 'match not found')
        m.finished = True
        rounds = json.loads(m.rounds_data or '[]')
        m.result_summary = f'rounds={len(rounds)}'
        s.add(m); s.commit()
        return {'ok': True}
