import numpy as np
from PIL import Image


def _smooth_noise(size, cells, rng):
    grid = rng.random((cells + 1, cells + 1), dtype=np.float32)
    coords = np.linspace(0, cells, size, endpoint=False)
    x0 = coords.astype(np.int32)
    y0 = coords.astype(np.int32)
    xf = coords - x0
    yf = coords - y0
    xf = xf * xf * (3.0 - 2.0 * xf)
    yf = yf * yf * (3.0 - 2.0 * yf)
    a = grid[y0[:, None], x0[None, :]]
    b = grid[y0[:, None], x0[None, :] + 1]
    c = grid[y0[:, None] + 1, x0[None, :]]
    d = grid[y0[:, None] + 1, x0[None, :] + 1]
    top = a * (1 - xf[None, :]) + b * xf[None, :]
    bottom = c * (1 - xf[None, :]) + d * xf[None, :]
    return top * (1 - yf[:, None]) + bottom * yf[:, None]


def generate_texture(material="concrete", size=512, scale=0.55, noise=0.45,
                     detail=0.55, seed=None):
    """Generate an RGB procedural material texture."""
    size = int(size)
    if size not in (256, 512, 1024, 2048):
        raise ValueError("Resolution must be 256, 512, 1024 or 2048.")
    if material not in ("concrete", "wood", "metal", "wallpaper"):
        raise ValueError(f"Unknown material: {material}")

    rng = np.random.default_rng(seed)
    coarse = _smooth_noise(size, max(3, int(5 + scale * 30)), rng)
    fine = _smooth_noise(size, max(12, int(24 + detail * 120)), rng)
    grain = rng.random((size, size), dtype=np.float32)
    field = coarse * (0.72 - detail * 0.18) + fine * (0.18 + detail * 0.28)
    field += grain * (0.08 + noise * 0.28)
    field = np.clip((field - 0.5) * (0.9 + noise * 1.5) + 0.5, 0, 1)

    yy, xx = np.mgrid[0:size, 0:size].astype(np.float32)
    if material == "concrete":
        value = 0.34 + field * 0.30
        pores = (rng.random((size, size)) > (0.992 - detail * 0.012)).astype(np.float32)
        value = np.clip(value - pores * (0.12 + detail * 0.12), 0, 1)
        rgb = np.stack((value * 0.94, value * 0.97, value), axis=-1)
    elif material == "wood":
        waves = np.sin((xx / size * (8 + scale * 34) + coarse * (1.4 + detail * 3)) * 2 * np.pi)
        value = np.clip(0.30 + (waves * 0.5 + 0.5) * 0.36 + (fine - 0.5) * noise * 0.22, 0, 1)
        rgb = np.stack((value, value * 0.66, value * 0.38), axis=-1)
    elif material == "metal":
        brushed = np.sin((yy / size * (35 + scale * 110) + fine * detail * 2) * 2 * np.pi)
        value = np.clip(0.36 + field * 0.28 + brushed * (0.025 + detail * 0.035), 0, 1)
        scratches = (rng.random((size, size)) > (0.997 - detail * 0.008)).astype(np.float32)
        value = np.clip(value - scratches * 0.22, 0, 1)
        rgb = np.stack((value * 0.84, value * 0.90, value), axis=-1)
    else:
        frequency = 5 + int(scale * 13)
        pattern = (np.sin(xx / size * frequency * 2 * np.pi) *
                   np.sin(yy / size * frequency * 2 * np.pi) * 0.5 + 0.5)
        value = np.clip(0.58 + pattern * 0.22 + (field - 0.5) * noise * 0.18, 0, 1)
        rgb = np.stack((value, value * 0.88, value * 0.65), axis=-1)

    return Image.fromarray(np.clip(rgb * 255, 0, 255).astype(np.uint8), "RGB")
