"""Water level vs. flood area percentage - rising-water impact analysis."""
from __future__ import annotations

from pathlib import Path

import numpy as np

from flood_inundation import flood_area_pct, load_dem, validate_monotonic_area

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ModuleNotFoundError:
    plt = None
    MATPLOTLIB_AVAILABLE = False

OUT_DIR = Path(__file__).resolve().parent
FIG_PATH = OUT_DIR / "flood_trend_curve.png"


def plot_with_matplotlib(water_levels: np.ndarray, area_pcts: np.ndarray) -> None:
    fig, ax = plt.subplots(figsize=(8, 5))
    ax.plot(water_levels, area_pcts, "b-o", markersize=4, linewidth=1.5)
    ax.fill_between(water_levels, 0, area_pcts, alpha=0.1, color="blue")
    ax.set_xlabel("Water Level (m)")
    ax.set_ylabel("Flooded Area (%)")
    ax.set_title(f"Water Level vs. Inundation Area ({water_levels[0]:.0f}-{water_levels[-1]:.0f} m)")
    ax.grid(True, alpha=0.3)

    for wl, pct in [(water_levels[0], area_pcts[0]), (water_levels[-1], area_pcts[-1])]:
        ax.annotate(f"WL={wl:.0f}m, {pct:.1f}%", xy=(wl, pct),
                    xytext=(wl + 0.5, pct - 3), fontsize=9,
                    arrowprops=dict(arrowstyle="->", color="grey"))

    fig.tight_layout()
    fig.savefig(FIG_PATH, dpi=150)
    plt.close(fig)


def plot_with_pillow(water_levels: np.ndarray, area_pcts: np.ndarray) -> None:
    from PIL import Image, ImageDraw, ImageFont

    width, height = 900, 560
    x0, y0, w, h = 90, 70, 740, 360
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()

    xmin, xmax = float(water_levels.min()), float(water_levels.max())
    ymin, ymax = 0.0, max(100.0, float(area_pcts.max()) * 1.1)

    def scale(x, y):
        px = x0 + (float(x) - xmin) / (xmax - xmin) * w
        py = y0 + h - (float(y) - ymin) / (ymax - ymin) * h
        return px, py

    draw.text((x0, 25), "Water Level vs. Inundation Area", fill="#111111", font=font)
    draw.rectangle((x0, y0, x0 + w, y0 + h), outline="#222222", width=2)
    for i in range(1, 5):
        draw.line((x0 + i * w / 5, y0, x0 + i * w / 5, y0 + h), fill="#eeeeee")
        draw.line((x0, y0 + i * h / 5, x0 + w, y0 + i * h / 5), fill="#eeeeee")

    points = [scale(wl, ap) for wl, ap in zip(water_levels, area_pcts)]
    draw.line(points, fill="#2166ac", width=3)
    for point in points:
        x, y = point
        draw.ellipse((x - 4, y - 4, x + 4, y + 4), fill="#2166ac")

    draw.text((x0 + w // 2 - 45, y0 + h + 34), "Water Level (m)", fill="#222222", font=font)
    draw.text((16, y0 + 12), "Flooded Area (%)", fill="#222222", font=font)
    draw.text((x0, y0 + h + 12), f"{xmin:.1f}", fill="#333333", font=font)
    draw.text((x0 + w - 30, y0 + h + 12), f"{xmax:.1f}", fill="#333333", font=font)
    draw.text((x0 - 42, y0 + h - 6), "0", fill="#333333", font=font)
    draw.text((x0 - 48, y0 - 6), f"{ymax:.0f}", fill="#333333", font=font)
    draw.text((x0 + 15, y0 + 15), f"Start: {area_pcts[0]:.2f}%", fill="#2166ac", font=font)
    draw.text((x0 + 15, y0 + 35), f"End: {area_pcts[-1]:.2f}%", fill="#2166ac", font=font)

    img.save(FIG_PATH)


def main() -> None:
    dem = load_dem()
    wl_start, wl_end, wl_step = 40.0, 50.0, 0.5
    water_levels = np.arange(wl_start, wl_end + wl_step, wl_step)
    area_pcts = np.array([flood_area_pct(dem < wl) for wl in water_levels])

    if MATPLOTLIB_AVAILABLE:
        plot_with_matplotlib(water_levels, area_pcts)
    else:
        plot_with_pillow(water_levels, area_pcts)

    print(f"{'WL(m)':>7}  {'Area%':>8}  {'Delta%':>8}")
    print("-" * 28)
    for i, (wl, ap) in enumerate(zip(water_levels, area_pcts)):
        delta = area_pcts[i] - area_pcts[i - 1] if i > 0 else 0
        marker = " <<<" if wl == wl_start or wl == wl_end else ""
        print(f"{wl:6.1f}  {ap:7.2f}%  {delta:+7.2f}%{marker}")

    results = [{"water_level_m": float(wl), "area_pct": float(ap)}
               for wl, ap in zip(water_levels, area_pcts)]
    print(f"\nMonotonic increase: {'PASS' if validate_monotonic_area(results) else 'FAIL'}")
    print(f"Total increase: {area_pcts[-1] - area_pcts[0]:.1f} pp "
          f"({area_pcts[-1] / area_pcts[0]:.1f}x)")
    print(f"Saved: {FIG_PATH}")


if __name__ == "__main__":
    main()
