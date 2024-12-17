[app]
# (str) Title of your application
title = 好习惯追踪器

# (str) Package name
package.name = habittracker

# (str) Package domain (needed for android/ios packaging)
package.domain = org.habit

# (str) Source code where the main.py live
source.dir = .

# (list) Source files to include (let empty to include all the files)
source.include_exts = py,png,jpg,kv,atlas,ttf,db,otf

# (list) Source files to include (let empty to include all the files)
source.include_patterns = fonts/*

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_dirs = tests, bin, .git, __pycache__, .github, .buildozer

# (list) List of directory to exclude (let empty to not exclude anything)
source.exclude_patterns = Thumbs.db

# (str) Application versioning (method 1)
version = 1.0

# (list) Application requirements
requirements = python3,kivy,sqlite3,pillow,plyer

# (str) Supported orientations (one of landscape, portrait or all)
orientation = portrait

# (int) Fullscreen (0 to show menu) (1 to not show menu)
fullscreen = 0

# (list) Permissions
android.permissions = WRITE_EXTERNAL_STORAGE

# (str) Android NDK version to use
android.ndk = 25

# (int) Target Android API, should be as high as possible.
android.api = 33

# (int) Minimum API your APK will support.
android.minapi = 21

# (str) Android SDK version to use
android.sdk = 33

# (bool) Accept SDK license
android.accept_sdk_license = True

# (str) The Android arch to build for, choices: armeabi-v7a, arm64-v8a, x86
android.arch = arm64-v8a

# (bool) Allow the backup of your app's data on android devices.
android.allow_backup = True

# (str) XML file for custom backup rules (e.g. specifying storage paths, whether to backup to the external device, etc.)
android.backup_rules = backup_rules.xml

# (bool) Skip the Android SDK installation
android.skip_update = False

# (bool) Skip the Android NDK installation
android.skip_ndk_install = False

# (bool) Use --private data storage (True) or --dir public storage (False)
android.private_storage = True

# (str) Android logcat filters to use
android.logcat_filters = *:S python:D

# (bool) Copy library instead of making a libpymodules.so
android.copy_libs = 1

# (int) Android NDK API to use. This is the minimum API your app will support.
android.ndk_api = 21

[buildozer]
# (int) Log level (0 = error only, 1 = info, 2 = debug (with command output))
log_level = 2

# (int) Display warning if buildozer is run as root (0 = False, 1 = True)
warn_on_root = 0

# (str) Path to build artifact storage, absolute or relative to spec file
build_dir = ./.buildozer

# (str) Path to build output (i.e. .apk, .aab, .ipa) storage
bin_dir = ./bin
