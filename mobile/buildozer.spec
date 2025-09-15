[app]
# --- App Info ---
title = MCGG Xbot
package.name = mcgg_xbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# --- Dependencies ---
# Pastikan semua library yang dibutuhkan ada di sini.
# Buildozer akan mengurus instalasi setuptools, cython, dan wheel.
requirements = python3,kivy==2.2.1,requests,setuptools,cython,wheel

# --- Orientation ---
orientation = portrait

# --- Android Settings ---
android.api = 31
android.minapi = 21
# path ke SDK dan NDK akan diatur di GitHub Actions, jadi tidak perlu lagi di sini.
# android.sdk_path = /home/runner/.buildozer/android/platform/android-sdk
# android.ndk_path = /home/runner/.buildozer/android/platform/android-ndk-r25b
android.ndk_api = 21

# --- Python-for-Android ---
p4a.bootstrap = sdl2
# Kita sudah mengelola `p4a.branch` di `build.yml`, jadi baris ini tidak diperlukan.
# p4a.branch = develop

log_level = 2

# --- Keystore Config (untuk Release build) ---
android.release_keystore = ../mcgg-release-key.jks
android.release_keystore_password = ${P4A_RELEASE_KEYSTORE_PASSWD}
android.release_keyalias = ${P4A_RELEASE_KEYALIAS}
android.release_keyalias_password = ${P4A_RELEASE_KEYALIAS_PASSWD}
