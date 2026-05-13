"""Flood inundation analysis from a DEM and water level."""
import numpy as np
from pathlib import Path

OUT_DIR = Path(__file__).resolve().parent


def load_dem(path: str | Path = "dem_synthetic_100x100.npy") -> np.ndarray:
    """Load DEM from .npy file."""
    return np.load(OUT_DIR / path)


def flood_mask(dem: np.ndarray, water_level: float) -> np.ndarray:
    """Boolean mask: True where elevation < water_level."""
    return dem < water_level


def flood_depth(dem: np.ndarray, water_level: float) -> np.ndarray:
    """Depth array: water_level - elevation in flooded cells, 0 elsewhere."""
    depth = water_level - dem
    depth[depth < 0] = 0
    return depth


def flood_area_pct(mask: np.ndarray) -> float:
    """Percentage of cells that are flooded."""
    return mask.sum() / mask.size * 100


def flood_stats(dem: np.ndarray, water_level: float) -> dict:
    """All inundation metrics at a given water level in one call."""
    mask = flood_mask(dem, water_level)
    depth = flood_depth(dem, water_level)
    flooded = mask.sum()

    return {
        "water_level_m": water_level,
        "flooded_cells": flooded,
        "total_cells": mask.size,
        "area_pct": flooded / mask.size * 100,
        "max_depth_m": depth.max(),
        "mean_depth_m": depth[mask].mean() if flooded > 0 else 0.0,
        "total_volume_m3": depth.sum(),  # assuming 1×1 m cells
    }


# --- Demo ---
if __name__ == "__main__":
    dem = load_dem()
    levels = [40, 45, 50, 55, 60, 65, 70]

    print(f"{'Level(m)':>8}  {'Area%':>7}  {'MeanD(m)':>8}  {'MaxD(m)':>8}  {'Vol(m3)':>12}")
    print("-" * 55)
    for wl in levels:
        s = flood_stats(dem, wl)
        print(f"{s['water_level_m']:8.1f}  {s['area_pct']:6.2f}%  "
              f"{s['mean_depth_m']:8.2f}  {s['max_depth_m']:8.2f}  "
              f"{s['total_volume_m3']:12.0f}")

    # Detailed example at water_level = 55 m
    print("\n--- Detailed report at 55 m ---")
    wl = 55.0
    mask = flood_mask(dem, wl)
    depth = flood_depth(dem, wl)

    print(f"Mask dtype:  {mask.dtype}, shape: {mask.shape}")
    print(f"Depth dtype: {depth.dtype}, shape: {depth.shape}")
    print(f"Flooded:     {mask.sum()}/{mask.size} cells ({mask.sum()/mask.size*100:.1f}%)")
    print(f"Depth range: [{depth[depth > 0].min():.2f}, {depth.max():.2f}] m "
          f"(mean: {depth[depth > 0].mean():.2f} m)")
