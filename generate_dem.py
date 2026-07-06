"""Generate a synthetic 100×100 DEM with realistic terrain features."""
import numpy as np
from pathlib import Path

SIZE = 100
LOW, HIGH = 30.0, 80.0
SEED = 42
OUT_DIR = Path(__file__).resolve().parent
NPY_PATH = OUT_DIR / "dem_synthetic_100x100.npy"
CSV_PATH = OUT_DIR / "dem_synthetic_100x100.csv"
TIF_PATH = OUT_DIR / "dem_synthetic_100x100.tif"

rng = np.random.default_rng(SEED)

# --- Multi-scale noise for realistic terrain ---
def fbm_noise(size, octaves=6, lacunarity=2.0, gain=0.5, seed=SEED):
    """Fractional Brownian motion — layered noise that mimics real terrain."""
    rng_local = np.random.default_rng(seed)
    grid = np.zeros((size, size), dtype=np.float64)
    amplitude = 1.0
    frequency = 1.0
    max_val = 0.0
    for _ in range(octaves):
        # Low-res noise upscaled to full size via interpolation
        res = int(size * frequency)
        if res < 2:
            break
        coarse = rng_local.uniform(-1, 1, (res + 1, res + 1))
        # Bilinear upscale
        x = np.linspace(0, res, size)
        y = np.linspace(0, res, size)
        x_idx = np.floor(x).astype(int)
        y_idx = np.floor(y).astype(int)
        x_frac = x - x_idx
        y_frac = y - y_idx
        x_idx = np.clip(x_idx, 0, res - 1)
        y_idx = np.clip(y_idx, 0, res - 1)
        x_next = np.clip(x_idx + 1, 0, res)
        y_next = np.clip(y_idx + 1, 0, res)
        # Interpolate: bilinear over 2D
        layer = (
            coarse[np.ix_(y_idx, x_idx)] * (1 - x_frac)[None, :] * (1 - y_frac)[:, None]
            + coarse[np.ix_(y_idx, x_next)] * x_frac[None, :] * (1 - y_frac)[:, None]
            + coarse[np.ix_(y_next, x_idx)] * (1 - x_frac)[None, :] * y_frac[:, None]
            + coarse[np.ix_(y_next, x_next)] * x_frac[None, :] * y_frac[:, None]
        )
        grid += amplitude * layer
        max_val += amplitude
        amplitude *= gain
        frequency *= lacunarity
    return grid / max_val  # normalize to [-1, 1]

# Generate terrain
terrain = fbm_noise(SIZE)

# Add a gentle ridge line (optional) — makes it look more like real terrain
ridge = np.sin(np.linspace(0, 2 * np.pi, SIZE))  # horizontal ridge
terrain += 0.3 * ridge[None, :]

# Normalize to [0, 1], then scale to [LOW, HIGH]
terrain -= terrain.min()
terrain /= terrain.max()
dem = LOW + terrain * (HIGH - LOW)

print(f"DEM shape:       {dem.shape}")
print(f"Elevation range: [{dem.min():.2f}, {dem.max():.2f}] m")
print(f"Mean elevation:  {dem.mean():.2f} m")

# Save as .npy
np.save(NPY_PATH, dem.astype(np.float32))
print(f"Saved: {NPY_PATH}")

# Save as .csv
np.savetxt(CSV_PATH, dem, delimiter=",", fmt="%.2f",
           header=f"DEM 100x100, elevation range [{LOW}-{HIGH}] m, seed={SEED}")
print(f"Saved: {CSV_PATH}")

# Save as GeoTIFF if rasterio available
try:
    import rasterio
    from rasterio.transform import from_origin
    transform = from_origin(0, SIZE, 1, 1)  # top-left corner
    with rasterio.open(
        TIF_PATH, "w",
        driver="GTiff",
        height=SIZE, width=SIZE,
        count=1,
        dtype=np.float32,
        crs="EPSG:32633",  # UTM 33N (arbitrary, replace with real CRS)
        transform=transform,
    ) as dst:
        dst.write(dem.astype(np.float32), 1)
    print(f"Saved: {TIF_PATH}")
except ImportError:
    print("rasterio not installed — skipping GeoTIFF. Install with: pip install rasterio")

print("\nDone. Load with: dem = np.load('dem_synthetic_100x100.npy')")
