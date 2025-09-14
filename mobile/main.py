from kivy.app import App
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.lang import Builder
from api_client import API

KV = open('app.kv').read()

class MainScreen(Screen): pass

class MApp(App):
    def build(self):
        self.api = API()
        self.sm = Builder.load_string(KV)
        return self.sm

    def go_login(self):
        print('Open login UI - not implemented in prototype')

    def demo_start(self):
        players = ['You','P2','P3','P4','P5','P6','P7','P8']
        r = self.api.start_match(players)
        print('start_match response:', r.status_code, r.text)
if __name__ == '__main__':
    MApp().run()
  
