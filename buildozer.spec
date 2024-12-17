[app]
title = HabitTracker
package.name = habittracker
package.domain = org.habit

source.dir = .
source.include_exts = py,png,jpg,kv,atlas,ttf
source.exclude_dirs = tests, bin, .git, __pycache__, .github, .buildozer
source.exclude_patterns = buildozer.spec

version = 1.0
requirements = python3,kivy==2.2.1,plyer

# Android specific
android.permissions = WRITE_EXTERNAL_STORAGE
android.api = 28
android.minapi = 21
android.ndk = 23.1.7779620
android.archs = armeabi-v7a arm64-v8a
android.allow_backup = True
android.accept_sdk_license = True

[buildozer]
log_level = 2
warn_on_root = 0
