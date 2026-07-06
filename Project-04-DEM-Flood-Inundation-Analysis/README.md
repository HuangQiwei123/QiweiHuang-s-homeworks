# Project 04 - DEM Flood Inundation Analysis

## Overview

This project analyzes flood inundation using a synthetic 100 x 100 DEM. It computes which cells become flooded at different water levels, calculates flood depth, visualizes inundation extent, plots water-level response, and validates the physical consistency of the results.

## Objectives

- Generate a reproducible DEM dataset.
- Calculate inundation mask and flood depth from a water level.
- Visualize DEM, flooded area, and depth distribution.
- Analyze how flooded area changes as water level rises.
- Validate results with physical-sense checks.

## Workflow

```text
1. generate_dem.py
   Generate DEM data and save it as .npy and .csv.

2. flood_inundation.py
   Compute flood mask, depth, flooded area percentage, and volume.

3. visualize_flood.py
   Produce a multi-panel inundation figure.

4. flood_trend.py
   Plot the relationship between water level and flooded area.

5. validate_flood.py
   Check physical consistency and save validation arrays.
```

## File Description

| File or Folder | Purpose |
|---|---|
| `generate_dem.py` | Creates synthetic terrain data. |
| `dem_synthetic_100x100.npy` | DEM data for Python loading. |
| `dem_synthetic_100x100.csv` | DEM data for direct table viewing. |
| `flood_inundation.py` | Core inundation calculation functions. |
| `visualize_flood.py` | Generates flood map and depth visualization. |
| `flood_trend.py` | Generates water-level versus inundation-area curve. |
| `validate_flood.py` | Runs validation checks. |
| `write_report.py` | Produces report material. |
| `flood_inundation_plot.png` | Main flood visualization output. |
| `flood_trend_curve.png` | Flooded-area trend output. |
| `validation_results.npz` | Saved validation arrays. |
| `screenshots/` | Running and interaction screenshots. |
| `Experiment4_Flood_Inundation.docx` | Experiment report. |
| `Flood_Inundation_Analysis_Report.docx` | Additional flood analysis report. |
| `requirements.txt` | Dependencies for this project. |

## How to Run

```bash
cd Project-04-DEM-Flood-Inundation-Analysis
pip install -r requirements.txt
python generate_dem.py
python flood_inundation.py
python visualize_flood.py
python flood_trend.py
python validate_flood.py
```

## Validation Checks

The validation script checks:

- flooded area percentage remains between 0 and 100;
- flood depth is never negative;
- flooded cells and positive-depth cells are consistent;
- maximum depth matches water level minus minimum elevation;
- inundated area does not decrease when water level rises.

## Review Outputs

- `flood_inundation_plot.png`: main visualization for DEM, flood extent, and depth.
- `flood_trend_curve.png`: water level versus flooded area.
- `validation_results.npz`: data produced by validation.
- `Flood_Inundation_Analysis_Report.docx`: written report file.
