import os, requests

BASE = os.getenv("MCGG_API", "http://127.0.0.1:8000")

class API:
    def __init__(self):
        self.token = None

    def set_token(self, token):
        self.token = token

    def headers(self):
        if not self.token: return {}
        return {"Authorization": f"Bearer {self.token}"}

    def register(self, username, password):
        return requests.post(f"{BASE}/register", json={"username":username,"password":password})

    def login(self, username, password):
        return requests.post(f"{BASE}/login", json={"username":username,"password":password})

    def start_match(self, players):
        return requests.post(f"{BASE}/match/start", json={"players":players}, headers=self.headers())

    def predict(self, match_id, players):
        return requests.post(f"{BASE}/match/predict", json={"players":players, "match_id":match_id}, headers=self.headers())

    def round_update(self, match_id, round_name, opponent):
        return requests.post(f"{BASE}/match/round", json={"match_id":match_id, "round_name":round_name, "opponent":opponent}, headers=self.headers())

    def eliminate(self, match_id, eliminated):
        return requests.post(f"{BASE}/match/eliminate", json={"match_id":match_id, "eliminated":eliminated}, headers=self.headers())

    def finish(self, match_id):
        return requests.post(f"{BASE}/match/finish", params={"match_id":match_id}, headers=self.headers())
