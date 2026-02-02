[app]

# ========================
# 应用基本信息
# ========================
title = 微信转发器
package.name = wechatforwarder
package.domain = org.wechat
source.dir = .
source.main = main.py
version = 1.0.0
version.code = 1

# ========================
# 依赖要求
# ========================
requirements = python3

# ========================
# Python-for-Android (p4a) 配置
# 使用新语法替代已弃用的配置
# ========================
p4a.bootstrap = webview
android.archs = armeabi-v7a

# ========================
# Android 配置
# ========================
android.api = 33
android.minapi = 21
android.sdk = 33
android.ndk = 25b
android.ndk_api = 21
android.permissions = INTERNET, ACCESS_NETWORK_STATE

# ========================
# 构建配置
# ========================
log_level = 2
release = 0

# ========================
# 图形资源
# ========================
icon.filename = icon.png
presplash.filename = presplash.png
presplash.color = #4CAF50

# ========================
# 排除文件
# ========================
source.exclude_dirs = bin, .buildozer, .git, __pycache__, *.pyc, *.pyo

# ========================
# 调试配置
# ========================
android.debug = 1
android.allow_backup = true
android.allow_reload = true

# ========================
# 签名配置（调试模式）
# ========================
android.mode = debug
android.keystore = debug.keystore
android.keystorepass = android
android.keyalias = androiddebugkey
android.keyaliaspass = android