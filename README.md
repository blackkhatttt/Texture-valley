# Texture Valley 0.1.0

Texture Valley is a cross-platform procedural texture creator built with Python, Kivy, NumPy and Pillow.

## Features
- Procedural Concrete, Wood, Metal and Wallpaper materials
- 256, 512, 1024 and 2048 square output sizes
- Scale, Noise and Detail controls
- 2D texture preview
- PNG export
- Touch-friendly Kivy interface for Android and desktop

## Run on PC
Python 3.11 is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

## Automated builds
The GitHub Actions workflow **Build Texture Valley** runs on pushes to `main` and can also be started manually from the Actions tab.

When the workflow succeeds, it publishes:
- **Texture-Valley-Windows**: a Windows desktop build.
- **Texture-Valley-Android-APK**: a debug APK for Android.
- **Texture-Valley-PC-Source**: the Python source package.

Open the repository's **Actions** tab, select **Build Texture Valley**, and choose **Run workflow** to start a build manually. Download the outputs from the completed run's **Artifacts** section.

## Android local build
Android builds can also be made on Linux with Buildozer:

```bash
python -m pip install buildozer cython
buildozer android debug
```

The first build downloads Android SDK/NDK components and may take several minutes.

## Export location
PNG files are saved in the application's private data directory under `exports/`. A system file picker/share workflow is planned for a later release.

## Current scope
Version 0.1 provides procedural generation. AI generation, PBR map sets, advanced seamless tiling and 3D preview are planned for future versions; they are not included as active features yet.
