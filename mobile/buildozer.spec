[app]
# --- App Info ---
title = MCGG Xbot
package.name = mcgg_xbot
package.domain = org.mcgg
source.dir = .
source.include_exts = py,png,jpg,kv,atlas
version = 0.1

# --- Dependencies ---
# Jangan tambahkan sh>=2,<3 karena konflik dengan python-for-android
# sh yang benar otomatis dipasang oleh p4a (versi 1.x)
requirements = python3,kivy==2.2.1,requests,setuptools,cython,wheel

# --- Orientation ---
orientation = portrait

# --- Android Settings ---
android.api = 33
android.minapi = 21
android.ndk_api = 21

# --- Python-for-Android ---
p4a.bootstrap = sdl2
# p4a.branch = stable   # opsional, bisa aktifkan kalau ingin selalu ambil branch stable

# Logging level (1=errors, 2=info, 3=debug)
log_level = 2

# --- Keystore Config (untuk Release build) ---
android.release_keystore = ../mcgg-release-key.jks
android.release_keystore_password = ${P4A_RELEASE_KEYSTORE_PASSWD}
android.release_keyalias = ${P4A_RELEASE_KEYALIAS}
android.release_keyalias_password = ${P4A_RELEASE_KEYALIAS_PASSWD}

# --- (Opsional) Permissions tambahan ---
# android.permissions = INTERNET,ACCESS_NETWORK_STATE
