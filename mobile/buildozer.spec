[app]
# --- Info App ---
title = MCGG Xbot
package.name = mcggxbot
package.domain = org.mcgg
source.dir = .

# --- Resource ---
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,ttc,otf,txt,json,xml,ini,mp3,ogg,wav,mp4,h5,tflite,pt,csv,yaml
icon.filename = %(source.dir)s/assets/iconmcgg.png

version = 1.0.0

requirements = python3,kivy,requests,setuptools,cython,wheel

# --- UI Config ---
orientation = portrait
fullscreen = 1

# --- Permission ---
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO

# --- Dependencies ---
requirements = python3,kivy==2.2.1,requests,pillow,setuptools,cython,wheel

[buildozer]
log_level = 2
warn_on_root = 1

# --- Android ---
android.api = 33
android.minapi = 21
android.ndk_api = 21
p4a.bootstrap = sdl2
p4a.branch = master
android.sdk = 33
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.ndk_path = $HOME/.buildozer/android/platform/android-ndk-r25b
android.sdk_path = $HOME/.buildozer/android/platform/android-sdk

# --- Release Signing ---
android.release_keystore = ../mcgg-release-key.jks
android.release_keystore_password = ${P4A_RELEASE_KEYSTORE_PASSWD}
android.release_keyalias = ${P4A_RELEASE_KEYALIAS}
android.release_keyalias_password = ${P4A_RELEASE_KEYALIAS_PASSWD}
