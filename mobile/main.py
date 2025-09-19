from kivy.app import App
from kivy.uix.screenmanager import ScreenManager, Screen, FadeTransition
from kivy.storage.jsonstore import JsonStore
from kivy.uix.popup import Popup
from kivy.uix.label import Label
import requests, threading

API_URL = "http://127.0.0.1:8000"

store = JsonStore("user.json")

class LoginScreen(Screen):
    def do_login(self, username, password):
        def task():
            try:
                res = requests.post(f"{API_URL}/login", json={"username": username, "password": password})
                if res.status_code == 200:
                    data = res.json()
                    store.put("auth", token=data["access_token"], user=username)
                    self.manager.current = "dashboard"
                else:
                    self.show_error("Login gagal!")
            except Exception as e:
                self.show_error(str(e))
        threading.Thread(target=task).start()

    def show_error(self, msg):
        Popup(title="Error", content=Label(text=msg), size_hint=(0.8,0.4)).open()

class RegisterScreen(Screen):
    def do_register(self, username, password):
        def task():
            try:
                res = requests.post(f"{API_URL}/register", json={"username": username, "password": password})
                if res.status_code == 200:
                    self.manager.current = "login"
                else:
                    self.show_error("Register gagal!")
            except Exception as e:
                self.show_error(str(e))
        threading.Thread(target=task).start()

    def show_error(self, msg):
        Popup(title="Error", content=Label(text=msg), size_hint=(0.8,0.4)).open()

class DashboardScreen(Screen):
    pass

class McggApp(App):
    def build(self):
        sm = ScreenManager(transition=FadeTransition())
        sm.add_widget(LoginScreen(name="login"))
        sm.add_widget(RegisterScreen(name="register"))
        sm.add_widget(DashboardScreen(name="dashboard"))
        return sm

if __name__ == "__main__":
    McggApp().run()
