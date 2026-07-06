# Project 4 -- DEM-based Flood Inundation Analysis
### Software Development · Flood Modeling · 2026

---

`folder: project-4`

This project builds a DEM-based flood inundation analysis workflow. It generates a synthetic terrain grid, calculates inundation masks and water depth under different water levels, creates visual outputs, and validates the result with physical-sense checks.

---

## Physics

```text
flood mask    flooded[i,j] = 1 if z[i,j] < W
depth         d[i,j] = max(W - z[i,j], 0)
flooded area  A = flooded cells / total cells * 100%
```

`z[i,j]` is terrain elevation and `W` is water level.

---

## Project Details

| | |
|---|---|
| **Python files** | `generate_dem.py` · `flood_inundation.py` · `visualize_flood.py` · `flood_trend.py` · `validate_flood.py` · `write_report.py` |
| **Output files** | `dem_synthetic_100x100.npy` · `dem_synthetic_100x100.csv` · `flood_inundation_plot.png` · `flood_trend_curve.png` · `validation_results.npz` |
| **Documents** | `requirements.txt` · `README.md` · `Experiment4_Flood_Inundation.docx` · `Flood_Inundation_Analysis_Report.docx` |
| **Screenshots** | `screenshots/1.png` · `screenshots/2.png` · `screenshots/3.png` · `screenshots/4.png` · `screenshots/5.png` |
| **Dependencies** | `numpy` · `matplotlib` |

---

## Workflow

```text
generate_dem.py
  -> create 100 x 100 synthetic DEM

flood_inundation.py
  -> compute flood mask, depth, area percentage, and volume-like statistics

visualize_flood.py
  -> generate flood_inundation_plot.png

flood_trend.py
  -> generate flood_trend_curve.png

validate_flood.py
  -> test physical consistency and save validation_results.npz
```

---

## Validation Checks

```text
area percentage in [0, 100]       PASS
maximum depth formula             PASS
non-negative depth                PASS
mask-depth consistency            PASS
depth value equals W - DEM        PASS
flooded area monotonicity         PASS
```

---

## Run It

```bash
pip install -r requirements.txt
python generate_dem.py
python flood_inundation.py
python visualize_flood.py
python flood_trend.py
python validate_flood.py
```

---

## Review Notes

- `dem_synthetic_100x100.csv` allows direct inspection of the DEM values.
- `flood_inundation_plot.png` is the main visualization for terrain, flood extent, and depth.
- `flood_trend_curve.png` shows how inundated area responds to water-level rise.
- `Flood_Inundation_Analysis_Report.docx` contains the report version of the experiment.
