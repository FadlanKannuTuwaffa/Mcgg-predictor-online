# main.py
import os
import traceback
from kivy.config import Config
from kivy.utils import platform
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.boxlayout import BoxLayout
from kivy.core.window import Window

# Optional config
Config.set("input", "mouse", "mouse,multitouch_on_demand")

# Atur ukuran default jika dijalankan di desktop
if platform in ("linux", "win"):
    Window.size = (360, 640)

KV_FILENAME = "app.kv"

class RootWidget(BoxLayout):
    pass

class McggApp(App):
    def build(self):
        try:
            if os.path.exists(KV_FILENAME):
                Builder.load_file(KV_FILENAME)
            return RootWidget()
        except Exception:
            self._log_exception("Error during build()")
            return RootWidget()

    def on_start(self):
        try:
            # Jika ada inisialisasi tambahan, taruh di sini
            pass
        except Exception:
            self._log_exception("Error in on_start()")

    def _log_exception(self, header="Exception"):
        tb = traceback.format_exc()
        msg = f"{header}\n{tb}\n"
        print(msg)
        try:
            p = os.path.join(self.user_data_dir, "crash.log")
            os.makedirs(self.user_data_dir, exist_ok=True)
            with open(p, "a") as f:
                f.write(msg)
        except Exception:
            print("Gagal menulis crash log:", msg)

if __name__ == "__main__":
    McggApp().run()
