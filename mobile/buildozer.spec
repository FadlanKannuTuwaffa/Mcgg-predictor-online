[app]
title = MCGG Xbot
package.name = mcgg_xbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# Versi Python & dependensi
requirements = python3,kivy==2.2.1,requests

orientation = portrait

# Target SDK
android.api = 31
android.minapi = 21

# Jangan hardcode path NDK, biar ambil dari ENV (dari build.yml)
# android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
android.ndk_api = 21

# Optional: untuk build lebih cepat
p4a.branch = master
log_level = 2

# Signing APK via GitHub Actions secrets
android.release_keystore = ../mcgg-release-key.jks
android.release_keystore_password = ${env:P4A_RELEASE_KEYSTORE_PASSWD}
android.release_keyalias = ${env:P4A_RELEASE_KEYALIAS}
android.release_keyalias_password = ${env:P4A_RELEASE_KEYALIAS_PASSWD}
