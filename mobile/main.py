# --- mobile/main.py ---
import os, tempfile
from kivy.utils import platform

# Pastikan KIVY_HOME menunjuk ke folder yang bisa ditulis di Android
def get_writable_kivy_home():
    kivy_home = os.environ.get('KIVY_HOME')
    if kivy_home:
        try:
            os.makedirs(kivy_home, exist_ok=True)
            return kivy_home
        except Exception:
            pass
    if platform == 'android':
        try:
            from android.storage import app_storage_path
            path = os.path.join(app_storage_path(), '.kivy')
            os.makedirs(path, exist_ok=True)
            return path
        except Exception:
            pass
    path = os.path.join(tempfile.gettempdir(), 'kivy_home')
    try:
        os.makedirs(path, exist_ok=True)
    except Exception:
        pass
    return path

os.environ.setdefault('KIVY_HOME', get_writable_kivy_home())

# --- Import Kivy setelah KIVY_HOME aman ---
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen

# ======================
# Definisi Screen Classes
# ======================
class LoginScreen(Screen):
    status_msg = ""

    def on_login(self):
        # TODO: logika login
        self.status_msg = "Login ditekan"


class RegisterScreen(Screen):
    status_msg = ""

    def on_register(self):
        # TODO: logika register
        self.status_msg = "Register ditekan"


class DashboardScreen(Screen):
    status_msg = ""

    def start_predict(self):
        # TODO: logika prediksi
        self.status_msg = "Prediksi dimulai"


class MatchScreen(Screen):
    status_msg = ""

    def save_round(self):
        self.status_msg = "Babak disimpan"

    def mark_eliminated(self):
        self.status_msg = "Eliminasi ditandai"

    def next_round(self):
        self.status_msg = "Lanjut babak"

    def finish_match(self):
        self.status_msg = "Pertandingan selesai"


class AdminScreen(Screen):
    status_msg = ""

    def on_pre_enter(self):
        # TODO: logika refresh admin
        self.status_msg = "Data admin diperbarui"


# ======================
# KV Inline (isi app.kv penuh)
# ======================
KV = """
#:import dp kivy.metrics.dp

<TitleLabel@Label>:
    font_size: '20sp'
    bold: True
    color: 0,0,0,1

<CustomInput@TextInput>:
    size_hint_y: None
    height: dp(40)
    multiline: False
    padding: [10, 10]

<CustomButton@Button>:
    size_hint_y: None
    height: dp(44)
    background_normal: ''
    background_color: (0.2, 0.6, 0.86, 1)
    color: (1,1,1,1)
    font_size: '15sp'
    bold: True

<LoginScreen>:
    name: "login"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(10)
        TitleLabel:
            text: "MCGG Xbot"
            size_hint_y: None
            height: dp(40)
        CustomInput:
            id: username
            hint_text: "Username"
        CustomInput:
            id: password
            hint_text: "Password"
            password: True
        Label:
            text: root.status_msg
            size_hint_y: None
            height: self.texture_size[1]+10
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(10)
            CustomButton:
                text: "Login"
                on_release: root.on_login()
            CustomButton:
                text: "Register"
                on_release: app.root.current = "register"

<RegisterScreen>:
    name: "register"
    BoxLayout:
        orientation: "vertical"
        padding: dp(20)
        spacing: dp(10)
        TitleLabel:
            text: "Register"
        CustomInput:
            id: r_username
            hint_text: "Username"
        CustomInput:
            id: r_password
            hint_text: "Password"
            password: True
        Label:
            text: root.status_msg
            size_hint_y: None
            height: self.texture_size[1]+10
        CustomButton:
            text: "Daftar"
            on_release: root.on_register()
        CustomButton:
            text: "Kembali"
            on_release: app.root.current = "login"

<DashboardScreen>:
    name: "dashboard"
    BoxLayout:
        orientation: "vertical"
        TitleLabel:
            text: "Dashboard"
        Label:
            text: "Selamat datang di dashboard!"
        GridLayout:
            cols: 2
            spacing: dp(8)
            size_hint_y: None
            height: self.minimum_height
            Label:
                text: "Player 1"
            CustomInput:
                id: p1
            Label:
                text: "Player 2"
            CustomInput:
                id: p2
            Label:
                text: "Player 3"
            CustomInput:
                id: p3
            Label:
                text: "Player 4"
            CustomInput:
                id: p4
            Label:
                text: "Player 5"
            CustomInput:
                id: p5
            Label:
                text: "Player 6"
            CustomInput:
                id: p6
            Label:
                text: "Player 7"
            CustomInput:
                id: p7
            Label:
                text: "Player 8"
            CustomInput:
                id: p8
        CustomButton:
            text: "Mulai Prediksi"
            on_release: root.start_predict()
        Label:
            id: pred_text
            text: ""
            size_hint_y: None
            height: self.texture_size[1]+10
        Label:
            text: root.status_msg
            size_hint_y: None
            height: self.texture_size[1]+10

<MatchScreen>:
    name: "match"
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(8)
        TitleLabel:
            text: "Match Tracker"
            size_hint_y: None
            height: dp(36)
        Label:
            id: round_label
            text: "Babak: I-II"
            size_hint_y: None
            height: dp(28)
        CustomInput:
            id: opponent_input
            hint_text: "Nama lawan (saat babak ini)"
        CustomButton:
            text: "Simpan Lawan"
            on_release: root.save_round()
        CustomInput:
            id: elim_input
            hint_text: "Nama pemain dieliminasi"
        CustomButton:
            text: "Tandai Eliminasi"
            on_release: root.mark_eliminated()
        BoxLayout:
            size_hint_y: None
            height: dp(48)
            spacing: dp(10)
            CustomButton:
                text: "Lanjut Babak"
                on_release: root.next_round()
            CustomButton:
                text: "Selesai Pertandingan"
                on_release: root.finish_match()
        Label:
            text: root.status_msg
            size_hint_y: None
            height: self.texture_size[1]+10

<AdminScreen>:
    name: "admin"
    BoxLayout:
        orientation: "vertical"
        padding: dp(12)
        spacing: dp(8)
        TitleLabel:
            text: "Admin Panel"
        ScrollView:
            do_scroll_x: False
            BoxLayout:
                orientation: "vertical"
                size_hint_y: None
                height: self.minimum_height
                RecycleBoxLayout:
                    default_size: None, dp(48)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    orientation: "vertical"
                    id: user_list
        CustomButton:
            text: "Refresh"
            on_release: root.on_pre_enter()
        Label:
            text: root.status_msg
            size_hint_y: None
            height: self.texture_size[1]+10

ScreenManager:
    LoginScreen:
    RegisterScreen:
    DashboardScreen:
    MatchScreen:
    AdminScreen:
"""

# ======================
# App utama
# ======================
class MyApp(App):
    def build(self):
        return Builder.load_string(KV)


if __name__ == "__main__":
    MyApp().run()
