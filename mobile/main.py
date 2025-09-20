# mobile/main.py (patched & full)
import threading
import requests
import time
from datetime import datetime
import os
import tempfile
from kivy.utils import platform

# -------------------------------------------------------------------------
# Perbaikan: pastikan KIVY_HOME ada di folder yang writable (Android & PC)
# -------------------------------------------------------------------------
def get_writable_kivy_home():
    # Jika sudah ada env var dan bisa dipakai → gunakan
    kivy_home = os.environ.get('KIVY_HOME')
    if kivy_home:
        try:
            os.makedirs(kivy_home, exist_ok=True)
            return kivy_home
        except Exception:
            pass

    # Kalau Android → pakai storage path bawaan aplikasi
    if platform == 'android':
        try:
            from android.storage import app_storage_path
            kivy_home = os.path.join(app_storage_path(), '.kivy')
            os.makedirs(kivy_home, exist_ok=True)
            return kivy_home
        except Exception:
            pass

    # Kalau gagal → pakai temp dir
    try:
        kivy_home = os.path.join(tempfile.gettempdir(), 'kivy_home')
        os.makedirs(kivy_home, exist_ok=True)
        return kivy_home
    except Exception:
        # Last resort → cwd
        kivy_home = os.path.join(os.getcwd(), '.kivy')
        try:
            os.makedirs(kivy_home, exist_ok=True)
        except Exception:
            pass
        return kivy_home


kivy_home = get_writable_kivy_home()
os.environ.setdefault('KIVY_HOME', kivy_home)

# -------------------------------------------------------------------------
# Perbaikan: Load app.kv dari beberapa lokasi (dev + setelah build)
# -------------------------------------------------------------------------
here = os.path.dirname(__file__) if '__file__' in globals() else os.getcwd()
kv_candidates = [
    os.path.join(here, 'app.kv'),           # posisi saat sudah dipaketkan
    os.path.join(here, 'mobile', 'app.kv'), # posisi saat development
    'app.kv',                               # fallback
]

KV = None
for path in kv_candidates:
    try:
        if path and os.path.exists(path):
            with open(path, 'r', encoding='utf-8') as f:
                KV = f.read()
            break
    except Exception:
        pass

if KV is None:
    # Coba ambil dengan pkgutil (jika app.kv dipaketkan sebagai resource)
    try:
        import pkgutil
        data = pkgutil.get_data(__package__ or '', 'app.kv')
        if data:
            KV = data.decode('utf-8')
    except Exception:
        pass

if KV is None:
    raise FileNotFoundError(f"app.kv not found. Looked in: {kv_candidates}")

# -------------------------------------------------------------------------
# Import & app logic asli Anda
# -------------------------------------------------------------------------
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.clock import Clock

# Inisialisasi UI dari KV string
Builder.load_string(KV)


# ------------------------
# Screen Definitions
# ------------------------
class HomeScreen(Screen):
    pass


class PredictScreen(Screen):
    pass


class ResultScreen(Screen):
    pass


class RootWidget(ScreenManager):
    pass


# ------------------------
# App Class
# ------------------------
class PredictorApp(App):
    def build(self):
        return RootWidget()

    def on_start(self):
        # Contoh: update waktu tiap detik di label dengan id 'time_label' di kv
        Clock.schedule_interval(self.update_time, 1)

    def update_time(self, *args):
        try:
            screen = self.root.get_screen('home')
            if hasattr(screen.ids, 'time_label'):
                screen.ids.time_label.text = datetime.now().strftime("%H:%M:%S")
        except Exception:
            pass


# ------------------------
# Main Entry
# ------------------------
if __name__ == "__main__":
    PredictorApp().run()
