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

# Build options
android.accept_sdk_license = True
android.gradle_dependencies = org.jetbrains.kotlin:kotlin-stdlib-jdk7:1.3.50
android.copy_libs = 1

# Gradle configuration
android.gradle_dependencies = org.jetbrains.kotlin:kotlin-stdlib-jdk7:1.3.50
android.enable_androidx = True

[buildozer]
log_level = 2
warn_on_root = 0
