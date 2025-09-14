[app]
title = MCGG Xbot
package.name = mcgg_xbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1
requirements = python3==3.10.8, kivy==2.2.1, requests
orientation = portrait

# Target SDK
android.api = 31
android.minapi = 21

# NDK stabil (r25b)
android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
android.ndk_api = 21

# Optional: untuk build lebih cepat
p4a.branch = master
log_level = 2

# Sign APK (ambil dari secret GitHub)
android.release_keystore = %(source.dir)s/../mcgg-release-key.jks
android.release_keystore_password = @string/KEYSTORE_PASSWORD
android.release_keyalias = @string/KEY_ALIAS
android.release_keyalias_password = @string/KEY_PASSWORD
