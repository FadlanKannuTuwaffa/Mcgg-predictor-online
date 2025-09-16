[app]
title = MCGG Xbot
package.name = mcggxbot
package.domain = org.mcgg
source.dir = .

# Resource yang dibundle
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,ttc,otf,txt,json,xml,ini,mp3,ogg,wav,mp4,h5,tflite,pt,csv,yaml

version = 1.0.0

# Icon aplikasi (pastikan file ada di mobile/assets/iconmcgg.png)
icon.filename = %(source.dir)s/assets/iconmcgg.png

# Konfigurasi orientasi & fullscreen
orientation = portrait
fullscreen = 1

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO

# Dependencies
requirements = python3, kivy==2.2.1, requests, pillow, sdl2, sdl2_image, sdl2_mixer, sdl2_ttf

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
