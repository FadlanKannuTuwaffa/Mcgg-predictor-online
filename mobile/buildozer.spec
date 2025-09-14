[app]
title = MCGG-Xbot_V.0.1
package.name = mcgg_xbot
package.domain = org.mcgg.xbot
source.dir = .
source.include_exts = py,kv,png,jpg
version = 0.1
requirements = python3,kivy,requests
orientation = portrait
fullscreen = 0
android.permissions = INTERNET,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE
android.archs = arm64-v8a, armeabi-v7a
android.release_keystore = mcgg-release-key.jks
android.release_keystore_pass = xbot234
android.release_keyalias = mcgg-xbot-key
android.release_keyalias_pass = xbot234
android.minapi = 21
android.ndk = 25b
android.build_tools_version = 33.0.2

[buildozer]
log_level = 2
warn_on_root = 1
