"""Visualize DEM, flood inundation, and depth for multiple water levels."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from flood_inundation import calculate_flood, load_dem

try:
    import matplotlib.colors as mcolors
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ModuleNotFoundError:
    mcolors = None
    plt = None
    MATPLOTLIB_AVAILABLE = False

OUT_DIR = Path(__file__).resolve().parent
FIG_PATH = OUT_DIR / "flood_inundation_plot.png"


def visualize_with_matplotlib(dem: np.ndarray, levels: list[float]) -> None:
    fig, axes = plt.subplots(3, len(levels), figsize=(16, 14))
    fig.suptitle("Flood Inundation Analysis - Synthetic DEM (100x100)", fontsize=16, y=0.98)

    flood_cmap = mcolors.ListedColormap(["#00000000", "#2166ac"])
    _ = flood_cmap

    for j, wl in enumerate(levels):
        mask, depth, area_pct = calculate_flood(dem, wl)

        ax0 = axes[0, j]
        im0 = ax0.imshow(dem, cmap=plt.cm.terrain, origin="lower")
        ax0.set_title(f"DEM - water level {wl} m")
        ax0.set_xlabel("Easting")
        ax0.set_ylabel("Northing")
        cbar0 = fig.colorbar(im0, ax=ax0, shrink=0.78)
        cbar0.set_label("Elevation (m)")

        ax1 = axes[1, j]
        ax1.imshow(dem, cmap="Greys", origin="lower", alpha=0.6)
        flood_rgba = np.zeros((*mask.shape, 4))
        flood_rgba[mask] = [0.13, 0.40, 0.67, 0.7]
        ax1.imshow(flood_rgba, origin="lower")
        ax1.set_title(f"Flood extent ({area_pct:.1f}% inundated) - WL {wl} m")
        ax1.set_xlabel("Easting")
        ax1.set_ylabel("Northing")

        ax2 = axes[2, j]
        masked_depth = np.where(depth > 0, depth, np.nan)
        ax2.imshow(dem, cmap="Greys", origin="lower", alpha=0.4)
        im3 = ax2.imshow(masked_depth, cmap=plt.cm.Blues, origin="lower")
        ax2.set_title(f"Flood depth (max {depth.max():.1f} m) - WL {wl} m")
        ax2.set_xlabel("Easting")
        ax2.set_ylabel("Northing")
        cbar2 = fig.colorbar(im3, ax=ax2, shrink=0.78)
        cbar2.set_label("Depth (m)")

    plt.tight_layout(rect=[0, 0, 1, 0.96])
    fig.savefig(FIG_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)


def _normalize(array: np.ndarray) -> np.ndarray:
    arr = np.asarray(array, dtype=float)
    span = arr.max() - arr.min()
    if span <= 1e-12:
        return np.zeros_like(arr)
    return (arr - arr.min()) / span


def _array_to_image(rgb: np.ndarray, scale: int = 3):
    from PIL import Image

    rgb_uint8 = np.clip(rgb * 255, 0, 255).astype(np.uint8)
    img = Image.fromarray(rgb_uint8, mode="RGB")
    return img.resize((rgb.shape[1] * scale, rgb.shape[0] * scale), Image.Resampling.NEAREST)


def visualize_with_pillow(dem: np.ndarray, levels: list[float]) -> None:
    from PIL import Image, ImageDraw, ImageFont

    scale = 3
    tile = dem.shape[0] * scale
    gap = 34
    left = 40
    top = 70
    width = left * 2 + len(levels) * tile + (len(levels) - 1) * gap
    height = top + 3 * tile + 3 * gap + 40
    canvas = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(canvas)
    font = ImageFont.load_default()

    dem_norm = _normalize(dem)
    terrain = np.dstack((0.25 + 0.55 * dem_norm, 0.45 + 0.35 * dem_norm, 0.25 + 0.15 * dem_norm))
    grey = np.dstack([0.25 + 0.55 * dem_norm] * 3)

    draw.text((left, 25), "Flood Inundation Analysis - Synthetic DEM (100x100)",
              fill="#111111", font=font)
    row_titles = ["DEM", "Flood extent", "Flood depth"]
    for r, title in enumerate(row_titles):
        draw.text((8, top + r * (tile + gap) + tile // 2), title, fill="#222222", font=font)

    for j, wl in enumerate(levels):
        mask, depth, area_pct = calculate_flood(dem, wl)
        depth_norm = _normalize(depth)
        extent = grey.copy()
        extent[mask] = [0.08, 0.35, 0.75]
        depth_rgb = grey.copy() * 0.45
        depth_rgb[mask] = np.dstack((
            0.12 + 0.10 * depth_norm,
            0.35 + 0.25 * depth_norm,
            0.70 + 0.25 * depth_norm,
        ))[mask]

        images = [
            _array_to_image(terrain, scale),
            _array_to_image(extent, scale),
            _array_to_image(depth_rgb, scale),
        ]
        x = left + j * (tile + gap)
        draw.text((x, top - 22), f"WL {wl} m | {area_pct:.1f}% flooded",
                  fill="#111111", font=font)
        for r, image in enumerate(images):
            y = top + r * (tile + gap)
            canvas.paste(image, (x, y))
            draw.rectangle((x, y, x + tile, y + tile), outline="#dddddd")

    canvas.save(FIG_PATH)


def main() -> None:
    dem = load_dem()
    levels = [45, 55, 65]
    if MATPLOTLIB_AVAILABLE:
        visualize_with_matplotlib(dem, levels)
    else:
        visualize_with_pillow(dem, levels)
    print(f"Saved: {FIG_PATH}")


if __name__ == "__main__":
    main()
