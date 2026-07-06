"""Visualize DEM, flood inundation, and depth for multiple water levels."""
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent

# --- Load DEM ---
dem = np.load(OUT_DIR / "dem_synthetic_100x100.npy")

# --- Helper: flood computations (same as flood_inundation.py) ---
def flood_mask(dem, wl):
    return dem < wl

def flood_depth(dem, wl):
    depth = wl - dem
    depth[depth < 0] = 0
    return depth

# --- Water levels to compare ---
levels = [45, 55, 65]

fig, axes = plt.subplots(3, len(levels), figsize=(16, 14))
fig.suptitle("Flood Inundation Analysis — Synthetic DEM (100\xd7100)", fontsize=16, y=0.98)

# Colormaps
dem_cmap = plt.cm.terrain
flood_cmap = mcolors.ListedColormap(["#00000000", "#2166ac"])  # transparent / blue
depth_cmap = plt.cm.Blues

for j, wl in enumerate(levels):
    mask = flood_mask(dem, wl)
    depth = flood_depth(dem, wl)
    area_pct = mask.sum() / mask.size * 100

    # --- Row 1: Raw DEM (grayscale) ---
    ax0 = axes[0, j]
    im0 = ax0.imshow(dem, cmap=dem_cmap, origin="lower")
    ax0.set_title(f"DEM — water level {wl} m")
    ax0.set_xlabel("Easting")
    ax0.set_ylabel("Northing")
    cbar0 = fig.colorbar(im0, ax=ax0, shrink=0.78)
    cbar0.set_label("Elevation (m)")

    # --- Row 2: Flood extent overlay (blue on DEM) ---
    ax1 = axes[1, j]
    ax1.imshow(dem, cmap="Greys", origin="lower", alpha=0.6)
    flood_rgba = np.zeros((*mask.shape, 4))
    flood_rgba[mask] = [0.13, 0.40, 0.67, 0.7]  # semi-transparent blue
    ax1.imshow(flood_rgba, origin="lower")
    ax1.set_title(f"Flood extent ({area_pct:.1f}% inundated) — WL {wl} m")
    ax1.set_xlabel("Easting")
    ax1.set_ylabel("Northing")

    # Legend patches
    import matplotlib.patches as mpatches
    dry_patch = mpatches.Patch(color="grey", alpha=0.5, label="Dry land")
    wet_patch = mpatches.Patch(color="#2166ac", alpha=0.7, label=f"Flooded ({area_pct:.1f}%)")
    ax1.legend(handles=[dry_patch, wet_patch], loc="upper right", fontsize=8)

    # --- Row 3: Flood depth heatmap ---
    ax2 = axes[2, j]
    masked_depth = np.where(depth > 0, depth, np.nan)
    im2 = ax2.imshow(dem, cmap="Greys", origin="lower", alpha=0.4)
    im3 = ax2.imshow(masked_depth, cmap=depth_cmap, origin="lower")
    ax2.set_title(f"Flood depth (max {depth.max():.1f} m) — WL {wl} m")
    ax2.set_xlabel("Easting")
    ax2.set_ylabel("Northing")
    cbar2 = fig.colorbar(im3, ax=ax2, shrink=0.78)
    cbar2.set_label("Depth (m)")

plt.tight_layout(rect=[0, 0, 1, 0.96])
fig_path = OUT_DIR / "flood_inundation_plot.png"
fig.savefig(fig_path, dpi=150, bbox_inches="tight")
print(f"Saved: {fig_path}")
plt.close(fig)
