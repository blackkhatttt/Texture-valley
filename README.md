# Texture Valley

Texture Valley is a procedural texture creator. The repository currently contains two editions:

- **Web edition** — browser-based app in `web/`, built with HTML, CSS and JavaScript. It requires no installation and can be deployed with GitHub Pages.
- **Python edition** — the original Kivy app for desktop and Android, kept intact as the native-app foundation.

## Web edition

Open `web/index.html` in a modern browser, or publish the `web/` folder with GitHub Pages.

The **Deploy Texture Valley Web** workflow deploys the site automatically when files in `web/` change on `main`. To enable the first deployment:

1. Open the repository's **Settings → Pages**.
2. Under **Build and deployment**, select **GitHub Actions** as the source.
3. Open **Actions** and run **Deploy Texture Valley Web** if the first push did not start it automatically.

The published address will be shown in the workflow's deployment environment after a successful run.

### Web 0.1.0 features

- Procedural Concrete, Wood, Metal and Wallpaper materials
- 256, 512, 1024 and 2048 square resolutions
- Scale, Noise and Detail controls
- Live 2D preview
- PNG export directly from the browser
- Responsive layout for desktop, tablet and mobile

## Python edition (original)

Python 3.11 is recommended.

```bash
python -m venv .venv
# Windows: .venv\\Scripts\\activate
# Linux/macOS: source .venv/bin/activate
pip install -r requirements.txt
python main.py
```

The original Kivy edition and its procedural generator remain in the repository. Android packaging is temporarily paused while the web edition is developed.

## Roadmap

- 0.1.0 — Web migration and core generator
- 0.2.0 — Editor improvements
- 0.3.0 — More procedural controls
- 0.4.0 — Texture library
- 0.5.0 — Export improvements
- 0.6.0 — Advanced materials
- 0.7.0 — Mobile optimization
- 0.8.0 — Additional tools
- 0.9.0 — Polish and testing
- 1.0.0 — Stable release

## Current scope

AI generation, PBR map sets, seamless tiling and 3D preview are future features, not part of Web 0.1.0.
