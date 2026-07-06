"""Water level vs. flood area percentage — rising-water impact analysis."""
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent
dem = np.load(OUT_DIR / "dem_synthetic_100x100.npy")

wl_start, wl_end, wl_step = 40.0, 50.0, 0.5
water_levels = np.arange(wl_start, wl_end + wl_step, wl_step)
area_pcts = np.array([(dem < wl).sum() / dem.size * 100 for wl in water_levels])

# --- Plot ---
fig, ax = plt.subplots(figsize=(8, 5))
ax.plot(water_levels, area_pcts, "b-o", markersize=4, linewidth=1.5)
ax.fill_between(water_levels, 0, area_pcts, alpha=0.1, color="blue")
ax.set_xlabel("Water Level (m)")
ax.set_ylabel("Flooded Area (%)")
ax.set_title(f"Water Level vs. Inundation Area  ({wl_start}–{wl_end} m)")
ax.grid(True, alpha=0.3)

# Annotate key thresholds
for wl, pct in [(wl_start, area_pcts[0]), (wl_end, area_pcts[-1])]:
    ax.annotate(f"WL={wl:.0f}m, {pct:.1f}%", xy=(wl, pct),
                xytext=(wl + 0.5, pct - 3), fontsize=9,
                arrowprops=dict(arrowstyle="->", color="grey"))

fig.tight_layout()
fig_path = OUT_DIR / "flood_trend_curve.png"
fig.savefig(fig_path, dpi=150)
plt.close(fig)

# --- Print table ---
print(f"{'WL(m)':>7}  {'Area%':>8}  {'Delta%':>8}")
print("-" * 28)
for i, (wl, ap) in enumerate(zip(water_levels, area_pcts)):
    delta = area_pcts[i] - area_pcts[i - 1] if i > 0 else 0
    marker = " <<<" if wl == wl_start or wl == wl_end else ""
    print(f"{wl:6.1f}  {ap:7.2f}%  {delta:+7.2f}%{marker}")

print(f"\nTotal increase: {area_pcts[-1] - area_pcts[0]:.1f} pp ({area_pcts[-1]/area_pcts[0]:.1f}x)")
print(f"Saved: {fig_path}")
