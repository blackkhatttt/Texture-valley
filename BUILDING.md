# Texture Valley — Automated builds

GitHub Actions builds the Android debug APK, the Windows desktop application, and a source ZIP whenever changes are pushed to `main`.

## Android
The Android job runs `buildozer android debug` and uploads the generated APK as the `Texture-Valley-Android-APK` workflow artifact.

## Windows
The Windows job packages the Kivy application with PyInstaller and uploads `Texture-Valley-Windows`.

## Source
The test job runs Python syntax checks and generator unit tests, then uploads `Texture-Valley-PC-Source`.

Open the Actions tab in the repository to inspect build status and download successful artifacts.