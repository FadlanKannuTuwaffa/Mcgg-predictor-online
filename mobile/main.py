# mobile/main.py
import threading
import requests
import time
from datetime import datetime
import os

# Set custom KIVY_HOME supaya tidak error "Permission denied" di Android
kivy_home = os.path.join(os.getcwd(), '.kivy')
os.environ.setdefault('KIVY_HOME', kivy_home)
try:
    os.makedirs(kivy_home, exist_ok=True)
except Exception:
    tmp = os.path.join('/data', 'local', 'tmp', 'kivy_home')
    os.environ['KIVY_HOME'] = tmp
    os.makedirs(tmp, exist_ok=True)

from kivy.app import App
from kivy.lang import Builder
from kivy.properties import StringProperty, ListProperty, BooleanProperty, NumericProperty
from kivy.clock import mainthread
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.storage.jsonstore import JsonStore

API_BASE = "http://127.0.0.1:8000"  # update ke URL backend kamu

# Simpan auth.json di dalam KIVY_HOME agar aman
store = JsonStore(os.path.join(os.environ.get("KIVY_HOME", "."), "auth.json"))

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
            # check admin flag from backend
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


class RootManager(ScreenManager):
    pass


class McggApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    McggApp().run()
