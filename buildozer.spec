[app]
title = Texture Valley
package.name = texturevalley
package.domain = org.texturevalley
source.dir = .
source.include_exts = py,png,jpg,kv,atlas,txt
version = 0.1.0
requirements = python3,kivy,numpy,pillow,charset-normalizer==2.1.1
orientation = portrait
fullscreen = 0

# Android build settings belong in [app] for Buildozer 1.5.
android.api = 35
android.minapi = 24
android.archs = arm64-v8a

[buildozer]
log_level = 2
warn_on_root = 1
