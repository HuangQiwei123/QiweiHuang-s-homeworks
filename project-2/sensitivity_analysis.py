from __future__ import annotations

from pathlib import Path

import numpy as np

from scs_cn import calculate_runoff

try:
    import matplotlib.pyplot as plt
    MATPLOTLIB_AVAILABLE = True
except ModuleNotFoundError:
    plt = None
    MATPLOTLIB_AVAILABLE = False

OUT_DIR = Path(__file__).resolve().parent
FIG_PATH = OUT_DIR / "scs_cn_sensitivity.png"


def plot_with_matplotlib(P_fixed: float, cn_values: list[float], P_range: np.ndarray) -> None:
    def plot_cn_vs_runoff(ax: plt.Axes) -> None:
        q_values = [calculate_runoff(P_fixed, cn) for cn in cn_values]
        ax.plot(cn_values, q_values, marker="o", linewidth=2, markersize=7, color="#2166ac")
        for cn, q in zip(cn_values, q_values):
            ax.annotate(f"{q:.1f}", (cn, q), textcoords="offset points",
                        xytext=(0, 10), ha="center", fontsize=8, color="#2166ac")
        ax.set_xlabel("Curve Number (CN)", fontsize=12)
        ax.set_ylabel("Runoff Q (mm)", fontsize=12)
        ax.set_title(f"SCS-CN Runoff Sensitivity (P = {P_fixed:.0f} mm)",
                     fontsize=13, fontweight="bold")
        ax.grid(True, linestyle="--", alpha=0.6)
        ax.set_xlim(55, 102)

    def plot_rainfall_vs_runoff(ax: plt.Axes) -> None:
        colors = ["#1b9e77", "#66a61e", "#e6ab02", "#d95f02", "#e7298a", "#7570b3"]
        for cn, color in zip(cn_values, colors):
            q_curve = calculate_runoff(P_range, cn)
            ax.plot(P_range, q_curve, linewidth=2, color=color, label=f"CN = {cn}")
        ax.plot(P_range, P_range, "--", linewidth=1, color="black",
                alpha=0.4, label="Q = P (CN=100 limit)")
        ax.set_xlabel("Precipitation P (mm)", fontsize=12)
        ax.set_ylabel("Runoff Q (mm)", fontsize=12)
        ax.set_title("Rainfall-Runoff Relationship by Curve Number",
                     fontsize=13, fontweight="bold")
        ax.legend(loc="upper left", fontsize=9, framealpha=0.9)
        ax.grid(True, linestyle="--", alpha=0.5)
        ax.set_xlim(0, max(P_range))
        ax.set_ylim(0, max(P_range) * 1.02)

    plt.rcParams.update({"figure.dpi": 120, "font.family": "sans-serif", "font.size": 10})
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.2))
    plot_cn_vs_runoff(ax1)
    plot_rainfall_vs_runoff(ax2)
    plt.tight_layout()
    plt.savefig(FIG_PATH, dpi=150, bbox_inches="tight")
    plt.close(fig)


def plot_with_pillow(P_fixed: float, cn_values: list[float], P_range: np.ndarray) -> None:
    from PIL import Image, ImageDraw, ImageFont

    width, height = 1200, 520
    img = Image.new("RGB", (width, height), "white")
    draw = ImageDraw.Draw(img)
    font = ImageFont.load_default()
    colors = ["#1b9e77", "#66a61e", "#e6ab02", "#d95f02", "#e7298a", "#7570b3"]

    def panel(x0, y0, w, h, title, xlabel, ylabel):
        draw.rectangle((x0, y0, x0 + w, y0 + h), outline="#222222", width=2)
        draw.text((x0, y0 - 28), title, fill="#111111", font=font)
        draw.text((x0 + w // 2 - 40, y0 + h + 30), xlabel, fill="#222222", font=font)
        draw.text((x0 - 78, y0 + 8), ylabel, fill="#222222", font=font)
        for i in range(1, 5):
            draw.line((x0 + i * w / 5, y0, x0 + i * w / 5, y0 + h), fill="#eeeeee")
            draw.line((x0, y0 + i * h / 5, x0 + w, y0 + i * h / 5), fill="#eeeeee")

    def scale(x, y, x0, y0, w, h, xmin, xmax, ymin, ymax):
        px = x0 + (float(x) - xmin) / (xmax - xmin) * w
        py = y0 + h - (float(y) - ymin) / (ymax - ymin) * h
        return px, py

    panel(90, 80, 430, 320, f"CN vs Runoff (P = {P_fixed:.0f} mm)",
          "Curve Number (CN)", "Runoff Q (mm)")
    q_values = [calculate_runoff(P_fixed, cn) for cn in cn_values]
    ymax = max(q_values) * 1.15 or 1.0
    pts = [scale(cn, q, 90, 80, 430, 320, 55, 102, 0, ymax)
           for cn, q in zip(cn_values, q_values)]
    draw.line(pts, fill="#2166ac", width=3)
    for cn, q, (x, y) in zip(cn_values, q_values, pts):
        draw.ellipse((x - 5, y - 5, x + 5, y + 5), fill="#2166ac")
        draw.text((x - 12, y - 20), f"{q:.1f}", fill="#2166ac", font=font)
        draw.text((x - 8, 410), f"{int(cn)}", fill="#333333", font=font)

    panel(680, 80, 430, 320, "Rainfall-Runoff by CN",
          "Precipitation P (mm)", "Runoff Q (mm)")
    for cn, color in zip(cn_values, colors):
        q_curve = calculate_runoff(P_range, cn)
        curve = [scale(p, q, 680, 80, 430, 320, 0, 100, 0, 100)
                 for p, q in zip(P_range, q_curve)]
        draw.line(curve, fill=color, width=2)
    draw.line((680, 400, 1110, 80), fill="#777777", width=1)
    for i, (cn, color) in enumerate(zip(cn_values, colors)):
        y = 90 + i * 18
        draw.line((930, y, 960, y), fill=color, width=3)
        draw.text((968, y - 6), f"CN={int(cn)}", fill="#222222", font=font)

    draw.text((90, 25), "SCS-CN Sensitivity Analysis", fill="#111111", font=font)
    img.save(FIG_PATH)
    print(f"Saved: {FIG_PATH} (Pillow fallback)")


def print_observations() -> None:
    print("""
SCS-CN Sensitivity Analysis - Observations
==========================================
1. Runoff increases nonlinearly with CN. High CN values produce much larger
   runoff for the same rainfall because retention and initial abstraction shrink.
2. No runoff occurs until rainfall exceeds Ia = 0.2*S, especially for low CN.
3. CN=100 is the impervious-surface ceiling, so Q equals P.
4. The Q <= P constraint remains satisfied across the plotted range.
""")


def main() -> None:
    P_fixed = 50.0
    cn_values = [60, 70, 80, 90, 95, 100]
    P_range = np.linspace(0, 100, 200)

    if MATPLOTLIB_AVAILABLE:
        plot_with_matplotlib(P_fixed, cn_values, P_range)
        print(f"Saved: {FIG_PATH}")
    else:
        plot_with_pillow(P_fixed, cn_values, P_range)
    print_observations()


if __name__ == "__main__":
    main()
