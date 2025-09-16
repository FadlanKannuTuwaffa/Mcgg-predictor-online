[app]
# --- App Info ---
title = MCGG Xbot
package.name = mcgg_xbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# --- Dependencies ---
# Jangan pakai sh>=2 karena konflik dengan p4a
requirements = python3,kivy==2.2.1,requests,setuptools,cython==0.29.36,wheel

# --- Orientation ---
orientation = portrait

# --- Android Settings ---
android.api = 33
android.minapi = 21
android.ndk_api = 21

# Force build to generate APK instead of AAB
android.release_artifact = apk
android.debug_artifact = apk

# --- Python-for-Android ---
p4a.bootstrap = sdl2
# p4a.branch = stable   # opsional, aktifkan kalau mau p4a stable branch

log_level = 2

# --- Keystore Config (untuk Release build) ---
android.release_keystore = ../mcgg-release-key.jks
android.release_keystore_password = ${P4A_RELEASE_KEYSTORE_PASSWD}
android.release_keyalias = ${P4A_RELEASE_KEYALIAS}
android.release_keyalias_password = ${P4A_RELEASE_KEYALIAS_PASSWD}

# --- Permissions (opsional) ---
# android.permissions = INTERNET,ACCESS_NETWORK_STATE
