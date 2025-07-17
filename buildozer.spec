[app]

# App name & identifier
title = My Application
package.name = myapp
package.domain = org.test

# 應用程式原始碼路徑與檔案類型
source.dir = .
source.include_exts = py,png,jpg,kv,atlas

# App 版本
version = 0.1

# Python 與 Kivy 相關依賴
requirements = python3,kivy,sqlite3,setuptools

# 螢幕方向與顯示
orientation = portrait
fullscreen = 0

# 權限設定
android.permissions = INTERNET

# 支援的 Android 架構
android.archs = armeabi-v7a, arm64-v8a

# APK 建置輸出型態
android.debug_artifact = apk
android.release_artifact = apk

# 啟用 SDL2 bootstrap
p4a.bootstrap = sdl2

# Android 額外設定
android.allow_backup = 1
android.copy_libs = 1

# 🔐 Release 簽章設定（CI 自動化打包 Release 用）
android.release = 1
android.keystore = my-release-key.keystore
android.keyalias = my-key-alias
android.keyalias_pass = your-keyalias-password
android.keystore_pass = your-keystore-password

# 記得把上面4個值對應替換成你 keystore 實際資訊
# 你也可以透過 GitHub Secrets 傳進來，自動由 Workflow 填寫


[ios]
# iOS 支援相關（可略過）
ios.kivy_ios_url = https://github.com/kivy/kivy-ios
ios.kivy_ios_branch = master
ios.ios_deploy_url = https://github.com/phonegap/ios-deploy
ios.ios_deploy_branch = 1.10.0
ios.codesign.allowed = false


[buildozer]
# 日誌等級（0=錯誤, 1=資訊, 2=除錯）
log_level = 2

# 是否在 root 執行時警告
warn_on_root = 1

# 自訂建置資料夾（選用）
# build_dir = ./.buildozer
# bin_dir = ./bin
