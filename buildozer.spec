[app]

# Title of your application
title = My Application

# Package name
package.name = myapp

# Package domain
package.domain = org.test

# Source code directory
source.dir = .

# File extensions to include
source.include_exts = py,png,jpg,kv,atlas

# Version
version = 0.1

# Application requirements
requirements = python3,kivy,sqlite3,setuptools


# Supported screen orientation
orientation = portrait

# Fullscreen mode (0 = windowed, 1 = fullscreen)
fullscreen = 0

# Android permissions
android.permissions = INTERNET

# Android architectures to build for
android.archs = arm64-v8a, armeabi-v7a

# Enable Android backup
android.allow_backup = True

# Copy library instead of packaging as libpymodules.so
android.copy_libs = 1

# Output format for debug builds
android.debug_artifact = apk

# Output format for release builds
android.release_artifact = apk

# Enable SDL2 bootstrap
p4a.bootstrap = sdl2

[ios]
# Optional: configure if you plan to support iOS
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false

[buildozer]

# Logging level (0 = error, 1 = info, 2 = debug)
log_level = 2

# Warn if running as root
warn_on_root = 1

# Optional: customize build directories
# build_dir = ./.buildozer
# bin_dir = ./bin
