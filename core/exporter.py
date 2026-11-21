from datetime import datetime
from pathlib import Path
import re


def export_texture(image, material="texture"):
    """Save a generated PNG in the app's private exports directory."""
    try:
        from kivy.app import App
        app = App.get_running_app()
        base = Path(app.user_data_dir) / "exports" if app else Path.cwd() / "exports"
    except Exception:
        base = Path.cwd() / "exports"

    base.mkdir(parents=True, exist_ok=True)
    safe_name = re.sub(r"[^a-z0-9_-]+", "_", str(material).lower()).strip("_") or "texture"
    filename = f"{safe_name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
    destination = base / filename
    image.save(destination, format="PNG")
    return str(destination)
