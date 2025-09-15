[app]
title = MCGG Xbot
package.name = mcgg_xbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Versi Python & library utama
requirements = python3,kivy==2.2.1,requests

# Orientasi layar
orientation = portrait

# Target SDK & NDK
android.api = 31
android.minapi = 21
android.sdk_path = $HOME/.buildozer/android/platform/android-sdk
android.ndk_path = $HOME/.buildozer/android/platform/android-ndk-r25b
android.ndk_api = 21

# Gunakan python-for-android branch terbaru
p4a.branch = master

# Logging lebih detail
log_level = 2

# Signing config (ambil dari secret GitHub Actions)
android.release_keystore = ../mcgg-release-key.jks
android.release_keystore_password = ${P4A_RELEASE_KEYSTORE_PASSWD}
android.release_keyalias = ${P4A_RELEASE_KEYALIAS}
android.release_keyalias_password = ${P4A_RELEASE_KEYALIAS_PASSWD}

# Pastikan SDL2 digunakan (lebih stabil untuk Kivy)
android.bootstrap = sdl2

# Opsi tambahan agar build stabil
# (misalnya force dikeluarkan, kalau nanti perlu kita bisa tambah modul lain)
