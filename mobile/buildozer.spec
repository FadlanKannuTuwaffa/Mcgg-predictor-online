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

# Android SDK/NDK
android.api = 31
android.minapi = 21
android.ndk_api = 21

# Biarkan Buildozer pakai SDK dari workflow
android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b

# Branch p4a
p4a.branch = master

# Logging lebih detail
log_level = 2

# Signing APK (keystore dari GitHub secrets)
android.release_keystore = ../mcgg-release-key.jks
android.release_keystore_password = ${P4A_RELEASE_KEYSTORE_PASSWD}
android.release_keyalias = ${P4A_RELEASE_KEYALIAS}
android.release_keyalias_password = ${P4A_RELEASE_KEYALIAS_PASSWD}
