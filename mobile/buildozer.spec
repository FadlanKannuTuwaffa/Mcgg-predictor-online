[app]
title = MCGG Xbot
package.name = mcggxbot
package.domain = org.mcgg
source.dir = .

# Pastikan semua resource ikut ke APK
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,ttc,otf,txt,json,xml,ini,mp3,ogg,wav,mp4,h5,tflite,pt,csv,yaml

version = 1.0.0

# Icon aplikasi
icon.filename = %(source.dir)s/assets/iconmcgg.png

# Orientasi aplikasi
orientation = portrait

# Permissions (tambah sesuai kebutuhan app kamu)
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE

# Requirements Python
requirements = python3, kivy, requests, pillow

[buildozer]
log_level = 2
warn_on_root = 1

# Android target
android.api = 31
android.minapi = 23
android.sdk = 31
android.ndk = 25b
android.archs = arm64-v8a, armeabi-v7a
android.ndk_path = $HOME/.buildozer/android/platform/android-ndk-r25b
android.sdk_path = $HOME/.buildozer/android/platform/android-sdk

# Packaging
p4a.release_keystore = ../mcgg-release-key.jks
p4a.release_keystore_passwd = your_keystore_password
p4a.release_keyalias = your_key_alias
p4a.release_keyalias_passwd = your_key_password

android.permissions = INTERNET,ACCESS_NETWORK_STATE,CAMERA,RECORD_AUDIO,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE
