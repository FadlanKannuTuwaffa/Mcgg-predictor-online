[app]
title = MCGG Xbot
package.name = mcgg_xbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

requirements = python3,kivy==2.2.1,requests

orientation = portrait

# Gunakan API 31 (sesuai workflow & Play Store minimum requirements sekarang 30+)
android.api = 31
android.minapi = 21
android.ndk_api = 21

# Jangan lock SDK/NDK path manual → biar pakai $ANDROID_HOME dari workflow
# android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
# android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

p4a.branch = master
p4a.bootstrap = sdl2
log_level = 2

# Signing (pakai secrets di GitHub Actions)
android.release_keystore = ../mcgg-release-key.jks
android.release_keystore_password = ${P4A_RELEASE_KEYSTORE_PASSWD}
android.release_keyalias = ${P4A_RELEASE_KEYALIAS}
android.release_keyalias_password = ${P4A_RELEASE_KEYALIAS_PASSWD}
