from fastapi import FastAPI, Depends, HTTPException, BackgroundTasks
from sqlmodel import Session, select
from .db import init_db, engine
from .models import Match, PredictionStat
from .schemas import *
from .auth import get_current_user
from .predictor import montecarlo_predict
from datetime import datetime
import json

app = FastAPI(title="MCGG-Xbot API")

@app.on_event("startup")
def on_start():
    init_db()

@app.get("/")
def root():
    return {"message": "FastAPI + Supabase + Render running!"}

@app.get("/me")
def me(user=Depends(get_current_user)):
    return {"id": user.id, "email": user.email}

@app.post('/match/start')
def start_match(data: PlayerListIn, user=Depends(get_current_user)):
    with Session(engine) as s:
        m = Match(user_id=user.id, rounds_data=json.dumps([]))
        s.add(m); s.commit(); s.refresh(m)
        return {'match_id': m.id, 'players': data.players}

@app.post('/match/predict')
def predict(payload: PlayerListIn, user=Depends(get_current_user)):
    players_list = payload.players
    if len(players_list) < 2:
        raise HTTPException(400, 'Need players')
    top2 = montecarlo_predict(players_list[0], players_list, sims=500)
    return {'predictions': top2}

@app.post('/match/round')
def round_update(data: RoundInput, user=Depends(get_current_user)):
    with Session(engine) as s:
        m = s.exec(select(Match).where(Match.id==data.match_id, Match.user_id==user.id)).first()
        if not m: raise HTTPException(404, 'match not found')
        rounds = json.loads(m.rounds_data or '[]')
        rounds.append({'round': data.round_name, 'opponent': data.opponent, 'ts': datetime.utcnow().isoformat()})
        m.rounds_data = json.dumps(rounds)
        s.add(m); s.commit()
        return {'ok': True, 'rounds': rounds}

@app.post('/match/eliminate')
def mark_elim(data: EliminateIn, user=Depends(get_current_user)):
    with Session(engine) as s:
        m = s.exec(select(Match).where(Match.id==data.match_id, Match.user_id==user.id)).first()
        if not m: raise HTTPException(404, 'match not found')
        rounds = json.loads(m.rounds_data or '[]')
        rounds.append({'event': 'eliminate', 'player': data.eliminated, 'ts': datetime.utcnow().isoformat()})
        m.rounds_data = json.dumps(rounds)
        s.add(m); s.commit()
        return {'ok': True}

@app.post('/match/finish')
def finish_match(match_id: int, user=Depends(get_current_user)):
    with Session(engine) as s:
        m = s.exec(select(Match).where(Match.id==match_id, Match.user_id==user.id)).first()
        if not m: raise HTTPException(404, 'match not found')
        m.finished = True
        rounds = json.loads(m.rounds_data or '[]')
        m.result_summary = f'rounds={len(rounds)}'
        s.add(m); s.commit()
        return {'ok': True}

@app.get('/stats')
def get_stats(user=Depends(get_current_user)):
    with Session(engine) as s:
        stats = s.exec(select(PredictionStat).where(PredictionStat.user_id==user.id)).all()
        return [{"key": st.key, "count": st.count} for st in stats]
