[app]
title = MCGG Xbot
package.name = mcgg_xbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3==3.10.8,kivy==2.2.1,requests

orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

# Android configs
android.api = 31
android.ndk = 25b
android.ndk_api = 23
android.arch = armeabi-v7a, arm64-v8a
android.sdk = 31
