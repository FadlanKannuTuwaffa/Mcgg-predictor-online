[app]
title = MCGG Xbot
package.name = mcggxbot
package.domain = org.mcgg
source.dir = .

# Resource yang dibundle
source.include_exts = py,png,jpg,jpeg,kv,atlas,ttf,ttc,otf,txt,json,xml,ini,mp3,ogg,wav,mp4,h5,tflite,pt,csv,yaml

version = 1.0.0

# Icon aplikasi
icon.filename = %(source.dir)s/assets/iconmcgg.png

# Orientasi & fullscreen
orientation = portrait
fullscreen = 1

# Permissions
android.permissions = INTERNET,ACCESS_NETWORK_STATE,READ_EXTERNAL_STORAGE,WRITE_EXTERNAL_STORAGE,CAMERA,RECORD_AUDIO

# Dependencies
requirements = python3, kivy==2.2.1, requests, pillow, sdl2, sdl2_image, sdl2_mixer, sdl2_ttf

[buildozer]
log_level = 2
warn_on_root = 1

# Android target (upgrade ke API 33)
android.api = 33
android.minapi = 23
android.ndk_api = 21

# Jangan override path, workflow yang handle
# android.ndk_path = $HOME/.buildozer/android/platform/android-ndk-r25b
# android.sdk_path = $HOME/.buildozer/android/platform/android-sdk

# Arsitektur
android.archs = arm64-v8a, armeabi-v7a
