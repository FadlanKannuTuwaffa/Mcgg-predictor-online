import os, requests

# Gunakan 10.0.2.2 agar Android Emulator bisa akses host machine
# Jika di device fisik, ubah ke IP LAN/WiFi server kamu, contoh: "http://192.168.1.5:8000"
BASE = os.getenv("MCGG_API", "http://10.0.2.2:8000")

class API:
    def __init__(self, base=None):
        self.base = base or BASE
        self.token = None

    def set_token(self, token):
        self.token = token

    def headers(self):
        return {"Authorization": f"Bearer {self.token}"} if self.token else {}

    def safe_post(self, path, **kwargs):
        try:
            return requests.post(f"{self.base}{path}", timeout=10, **kwargs)
        except requests.exceptions.RequestException as e:
            print("API request failed:", e)
            return None

    def register(self, username, password):
        return self.safe_post("/register", json={"username":username,"password":password})

    def login(self, username, password):
        return self.safe_post("/login", json={"username":username,"password":password})

    def start_match(self, players):
        return self.safe_post("/match/start", json={"players":players}, headers=self.headers())

    def predict(self, match_id, players):
        return self.safe_post("/match/predict", json={"players":players, "match_id":match_id}, headers=self.headers())

    def round_update(self, match_id, round_name, opponent):
        return self.safe_post("/match/round", json={"match_id":match_id, "round_name":round_name, "opponent":opponent}, headers=self.headers())

    def eliminate(self, match_id, eliminated):
        return self.safe_post("/match/eliminate", json={"match_id":match_id, "eliminated":eliminated}, headers=self.headers())

    def finish(self, match_id):
        return self.safe_post("/match/finish", params={"match_id":match_id}, headers=self.headers())
