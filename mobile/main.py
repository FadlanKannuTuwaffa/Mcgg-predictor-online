import threading
import requests
from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.clock import mainthread
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore

API_BASE = "http://127.0.0.1:8000"  # ganti dengan URL backend jika sudah deploy
store = JsonStore("auth.json")

KV = open("mobile/app.kv", "r", encoding="utf-8").read()


class BaseScreen(Screen):
    loading = BooleanProperty(False)
    status_msg = StringProperty("")


class LoginScreen(BaseScreen):
    def on_login(self):
        username = self.ids.username.text.strip()
        password = self.ids.password.text.strip()
        if not username or not password:
            self.status_msg = "Isi username dan password"
            return
        self.loading = True
        self.status_msg = "Mencoba login..."
        threading.Thread(target=self._login_thread, args=(username, password), daemon=True).start()

    def _login_thread(self, username, password):
        try:
            resp = requests.post(f"{API_BASE}/login", json={"username": username, "password": password}, timeout=20)
        except Exception as e:
            self._on_login_fail(f"Network error: {e}")
            return
        if resp.status_code == 200:
            data = resp.json()
            token = data.get("access_token")
            store.put("user", token=token, username=username)
            self._on_login_success()
        else:
            self._on_login_fail(f"{resp.status_code}: {resp.text}")

    @mainthread
    def _on_login_success(self):
        self.loading = False
        self.status_msg = "Login sukses!"
        App.get_running_app().root.current = "dashboard"
        self.ids.password.text = ""

    @mainthread
    def _on_login_fail(self, msg):
        self.loading = False
        self.status_msg = f"Gagal login: {msg}"


class RegisterScreen(BaseScreen):
    def on_register(self):
        username = self.ids.r_username.text.strip()
        password = self.ids.r_password.text.strip()
        if not username or not password:
            self.status_msg = "Isi username & password"
            return
        self.loading = True
        self.status_msg = "Mendaftar..."
        threading.Thread(target=self._reg_thread, args=(username, password), daemon=True).start()

    def _reg_thread(self, username, password):
        try:
            resp = requests.post(f"{API_BASE}/register", json={"username": username, "password": password}, timeout=20)
        except Exception as e:
            self._on_fail(f"Network error: {e}")
            return
        if resp.status_code in (200, 201):
            self._on_success("Akun terdaftar. Tunggu aktivasi admin.")
        else:
            self._on_fail(f"{resp.status_code}: {resp.text}")

    @mainthread
    def _on_success(self, msg):
        self.loading = False
        self.status_msg = msg
        App.get_running_app().root.current = "login"

    @mainthread
    def _on_fail(self, msg):
        self.loading = False
        self.status_msg = msg


class DashboardScreen(BaseScreen):
    username = StringProperty("")
    is_admin = BooleanProperty(False)

    def on_pre_enter(self):
        if store.exists("user"):
            tok = store.get("user")["token"]
            self.username = store.get("user")["username"]
            try:
                resp = requests.get(f"{API_BASE}/me", headers={"Authorization": f"Bearer {tok}"}, timeout=10)
                if resp.status_code == 200:
                    profile = resp.json()
                    self.is_admin = profile.get("is_admin", False)
                else:
                    self.is_admin = False
            except Exception:
                self.is_admin = False

    def logout(self):
        if store.exists("user"):
            store.delete("user")
        App.get_running_app().root.current = "login"


class PredictScreen(BaseScreen):
    players = ListProperty(["" for _ in range(8)])
    match_id = NumericProperty(0)
    predictions = ListProperty([])

    def on_pre_enter(self):
        for i in range(1, 8):
            self.ids[f"p{i+1}"].text = ""
        self.ids.p1.text = self.ids.p1.text or self.get_username_default()
        self.ids.p1.disabled = True
        self.predictions = []
        self.status_msg = ""

    def get_username_default(self):
        return store.get("user")["username"] if store.exists("user") else "Player1"

    def start_predict(self):
        names = []
        for i in range(1, 9):
            text = self.ids[f"p{i}"].text.strip()
            if i == 1:
                user = self.get_username_default()
                names.append(user)
            else:
                if not text:
                    self.status_msg = f"Isi nama player {i}"
                    return
                names.append(text)
        token = store.get("user")["token"]
        self.loading = True
        threading.Thread(target=self._predict_thread, args=(names, token), daemon=True).start()

    def _predict_thread(self, names, token):
        try:
            resp = requests.post(f"{API_BASE}/match/predict", json={"players": names}, headers={"Authorization": f"Bearer {token}"}, timeout=30)
        except Exception as e:
            self._predict_fail(f"Network error: {e}")
            return
        if resp.status_code == 200:
            preds = resp.json().get("predictions", [])
            try:
                resp2 = requests.post(f"{API_BASE}/match/start", json={"players": names}, headers={"Authorization": f"Bearer {token}"}, timeout=20)
                if resp2.status_code == 200:
                    mid = resp2.json().get("match_id")
                else:
                    mid = None
            except Exception:
                mid = None
            self._predict_success(preds, mid)
        else:
            self._predict_fail(f"{resp.status_code}: {resp.text}")

    @mainthread
    def _predict_success(self, preds, mid):
        self.loading = False
        self.predictions = preds
        self.match_id = mid or 0
        self.ids.pred_text.text = "\n".join([f"{p[0]} — {p[1]*100:.1f}%" for p in preds]) if preds else "Tidak ada prediksi"
        if mid:
            App.get_running_app().root.get_screen("match").match_id = mid
        App.get_running_app().root.current = "match"

    @mainthread
    def _predict_fail(self, msg):
        self.loading = False
        self.status_msg = msg


class MatchScreen(BaseScreen):
    rounds = ["I-II", "I-III", "I-IV", "Fatebox"]
    current_round = NumericProperty(0)
    match_id = NumericProperty(0)

    def on_pre_enter(self):
        self.ids.round_label.text = f"📍 Babak: {self.rounds[self.current_round]}"
        self.status_msg = ""

    def save_round(self):
        opp = self.ids.opponent_input.text.strip()
        if not opp:
            self.status_msg = "Isi nama lawan"
            return
        token = store.get("user")["token"]
        data = {"match_id": self.match_id, "round_name": self.rounds[self.current_round], "opponent": opp}
        try:
            resp = requests.post(f"{API_BASE}/match/round", json=data, headers={"Authorization": f"Bearer {token}"}, timeout=10)
            if resp.status_code == 200:
                self.status_msg = f"Lawan {opp} tersimpan"
                self.ids.opponent_input.text = ""
            else:
                self.status_msg = f"Error: {resp.status_code}"
        except Exception as e:
            self.status_msg = f"Network error: {e}"

    def mark_eliminated(self):
        elim = self.ids.elim_input.text.strip()
        if not elim:
            self.status_msg = "Isi nama yang dieliminasi"
            return
        token = store.get("user")["token"]
        try:
            resp = requests.post(f"{API_BASE}/match/eliminate", json={"match_id": self.match_id, "eliminated": elim}, headers={"Authorization": f"Bearer {token}"}, timeout=10)
            if resp.status_code == 200:
                self.status_msg = f"{elim} dieliminasi"
                self.ids.elim_input.text = ""
            else:
                self.status_msg = f"Error: {resp.status_code}"
        except Exception as e:
            self.status_msg = f"Network error: {e}"

    def next_round(self):
        if self.current_round < len(self.rounds) - 1:
            self.current_round += 1
            self.ids.round_label.text = f"📍 Babak: {self.rounds[self.current_round]}"
        else:
            self.status_msg = "Sudah di fase terakhir"

    def finish_match(self):
        token = store.get("user")["token"]
        try:
            resp = requests.post(f"{API_BASE}/match/finish", params={"match_id": self.match_id}, headers={"Authorization": f"Bearer {token}"}, timeout=10)
            if resp.status_code == 200:
                self.status_msg = "Pertandingan selesai"
            else:
                self.status_msg = f"Error: {resp.status_code}"
        except Exception as e:
            self.status_msg = f"Network error: {e}"


class AdminScreen(BaseScreen):
    users = ListProperty([])

    def on_pre_enter(self):
        token = store.get("user")["token"]
        try:
            resp = requests.get(f"{API_BASE}/admin/users", headers={"Authorization": f"Bearer {token}"}, timeout=10)
            if resp.status_code == 200:
                self.users = resp.json()
                self.status_msg = "Data user dimuat"
            else:
                self.status_msg = f"Error: {resp.status_code}"
        except Exception as e:
            self.status_msg = f"Network error: {e}"

    def approve(self, username):
        token = store.get("user")["token"]
        try:
            resp = requests.post(f"{API_BASE}/admin/approve/{username}", headers={"Authorization": f"Bearer {token}"}, timeout=10)
            if resp.status_code == 200:
                self.status_msg = f"{username} diaktifkan"
                self.on_pre_enter()
            else:
                self.status_msg = f"Error: {resp.status_code}"
        except Exception as e:
            self.status_msg = f"Network error: {e}"


class MCGGApp(App):
    def build(self):
        Builder.load_string(KV)
        sm = ScreenManager()
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        sm.add_widget(PredictScreen(name="predict"))
        sm.add_widget(MatchScreen(name="match"))
        sm.add_widget(AdminScreen(name="admin"))
        sm.current = "login" if not store.exists("user") else "dashboard"
        return sm


if __name__ == "__main__":
    MCGGApp().run()
