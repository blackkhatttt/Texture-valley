[app]
title = Texture Valley
package.name = texturevalley
package.domain = org.texturevalley
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 0.1.0
requirements = python3,kivy,numpy,pillow
orientation = portrait
fullscreen = 0

[buildozer]
log_level = 2
warn_on_root = 1

[android]
android.api = 35
android.minapi = 24
android.archs = arm64-v8a
android.accept_sdk_license = True
