from kivy.app import App
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivy.core.window import Window
from api_client import API

# Set warna background (putih agar tidak crash / blank)
Window.clearcolor = (1, 1, 1, 1)

class MainScreen(Screen):
    pass

class MApp(App):
    def build(self):
        self.api = API()
        # Load dari app.kv yang ikut dibundle
        return Builder.load_file("app.kv")

    def go_login(self):
        print('Open login UI - not implemented in prototype')

    def demo_start(self):
        players = ['You','P2','P3','P4','P5','P6','P7','P8']
        r = self.api.start_match(players)
        print('start_match response:', r.status_code, r.text)

if __name__ == '__main__':
    MApp().run()
