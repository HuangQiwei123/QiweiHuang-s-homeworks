"""Flood inundation analysis from a DEM and water level."""
from __future__ import annotations

from pathlib import Path

import numpy as np

OUT_DIR = Path(__file__).resolve().parent


def load_dem(path: str | Path = "dem_synthetic_100x100.npy") -> np.ndarray:
    """Load DEM data from a NumPy binary or CSV file."""
    dem_path = Path(path)
    if not dem_path.is_absolute():
        dem_path = OUT_DIR / dem_path
    if dem_path.suffix.lower() == ".csv":
        return np.loadtxt(dem_path, delimiter=",", comments="#")
    return np.load(dem_path)


def _validate_dem(dem: np.ndarray) -> np.ndarray:
    dem_array = np.asarray(dem, dtype=float)
    if dem_array.ndim != 2:
        raise ValueError("DEM must be a 2D array")
    if dem_array.size == 0:
        raise ValueError("DEM must not be empty")
    if not np.isfinite(dem_array).all():
        raise ValueError("DEM contains NaN or infinite elevations")
    return dem_array


def flood_mask(dem: np.ndarray, water_level: float) -> np.ndarray:
    """Boolean mask: True where elevation is lower than the water level."""
    return _validate_dem(dem) < water_level


def flood_depth(dem: np.ndarray, water_level: float) -> np.ndarray:
    """Depth array: water level minus elevation in flooded cells, 0 elsewhere."""
    dem_array = _validate_dem(dem)
    return np.maximum(water_level - dem_array, 0.0)


def flood_area_pct(mask: np.ndarray) -> float:
    """Percentage of cells that are flooded."""
    mask_array = np.asarray(mask, dtype=bool)
    if mask_array.size == 0:
        raise ValueError("Flood mask must not be empty")
    return float(mask_array.sum() / mask_array.size * 100.0)


def calculate_flood(
    dem: np.ndarray,
    water_level: float,
) -> tuple[np.ndarray, np.ndarray, float]:
    """Return flooded mask, depth array, and flooded area percentage."""
    mask = flood_mask(dem, water_level)
    depth = flood_depth(dem, water_level)
    return mask, depth, flood_area_pct(mask)


def flood_stats(dem: np.ndarray, water_level: float, cell_area_m2: float = 1.0) -> dict:
    """Return inundation metrics at a given water level."""
    if cell_area_m2 <= 0:
        raise ValueError("cell_area_m2 must be positive")

    mask, depth, area_pct = calculate_flood(dem, water_level)
    flooded = int(mask.sum())
    return {
        "water_level_m": float(water_level),
        "flooded_cells": flooded,
        "total_cells": int(mask.size),
        "area_pct": area_pct,
        "max_depth_m": float(depth.max()),
        "mean_depth_m": float(depth[mask].mean()) if flooded > 0 else 0.0,
        "total_volume_m3": float(depth.sum() * cell_area_m2),
    }


def simulate_rising_water(
    dem: np.ndarray,
    levels: np.ndarray | list[float],
    cell_area_m2: float = 1.0,
) -> list[dict]:
    """Calculate flood statistics for a sequence of rising water levels."""
    return [flood_stats(dem, float(level), cell_area_m2) for level in levels]


def validate_monotonic_area(results: list[dict]) -> bool:
    """Check that flooded area does not decrease as water level rises."""
    areas = np.array([row["area_pct"] for row in results], dtype=float)
    return bool(np.all(np.diff(areas) >= -1e-12))


if __name__ == "__main__":
    dem = load_dem()
    levels = [40, 45, 50, 55, 60, 65, 70]
    results = simulate_rising_water(dem, levels)

    print(f"{'Level(m)':>8}  {'Area%':>7}  {'MeanD(m)':>8}  {'MaxD(m)':>8}  {'Vol(m3)':>12}")
    print("-" * 55)
    for s in results:
        print(f"{s['water_level_m']:8.1f}  {s['area_pct']:6.2f}%  "
              f"{s['mean_depth_m']:8.2f}  {s['max_depth_m']:8.2f}  "
              f"{s['total_volume_m3']:12.0f}")
    print(f"\nMonotonic flooded area: {'PASS' if validate_monotonic_area(results) else 'FAIL'}")

    print("\n--- Detailed report at 55 m ---")
    wl = 55.0
    mask, depth, pct = calculate_flood(dem, wl)

    print(f"Mask dtype:  {mask.dtype}, shape: {mask.shape}")
    print(f"Depth dtype: {depth.dtype}, shape: {depth.shape}")
    print(f"Flooded:     {mask.sum()}/{mask.size} cells ({pct:.1f}%)")
    print(f"Depth range: [{depth[depth > 0].min():.2f}, {depth.max():.2f}] m "
          f"(mean: {depth[depth > 0].mean():.2f} m)")
