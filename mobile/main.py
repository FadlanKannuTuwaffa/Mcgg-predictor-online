from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from api_client import API

# Set warna background putih agar tidak blank/crash
Window.clearcolor = (1, 1, 1, 1)

class MainScreen(Screen):
    pass

class MApp(App):
    def build(self):
        self.api = API()
        # Load dari app.kv
        return Builder.load_file("app.kv")

    def go_login(self):
        print('Open login UI - not implemented in prototype')

    def demo_start(self):
        if not getattr(self, "api", None):
            print("API belum siap, skip start_match")
            return
        players = ['You','P2','P3','P4','P5','P6','P7','P8']
        r = self.api.start_match(players)
        if r is None:
            print("❌ start_match gagal: server tidak bisa dihubungi")
        else:
            print("✅ start_match response:", r.status_code, r.text)

if __name__ == '__main__':
    MApp().run()
