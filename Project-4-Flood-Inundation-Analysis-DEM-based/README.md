# Flood Inundation Analysis (DEM-based)

**Specialized Experiment 4 · Xi'an Jiaotong University · Software Development 2026**

DEM-based flood inundation analysis using a synthetic 100 x 100 terrain grid. The workflow generates terrain data, computes flooded area and depth for different water levels, visualizes flood extent, and validates physical consistency across rising-water scenarios.

---

## Flood Logic

| Metric | Rule |
| --- | --- |
| Flooded cell | `elevation < water_level` |
| Flood depth | `max(water_level - elevation, 0)` |
| Flooded area | `flooded_cells / total_cells * 100%` |
| Volume | `sum(depth) * cell_area` |
| Physical check | Flooded area must be non-decreasing as water level rises |

---

## What's Inside

| File | Role |
| --- | --- |
| `generate_dem.py` | Generates the synthetic DEM and exports `.npy` / `.csv` data |
| `flood_inundation.py` | Core flood mask, depth, area, volume, and rising-water functions |
| `visualize_flood.py` | Creates DEM, flood extent, and flood depth comparison figure |
| `flood_trend.py` | Plots water level vs. flooded area percentage |
| `validate_flood.py` | Runs physical-sense validation across 101 water levels |
| `write_report.py` | Generates the DOCX workflow report |
| `flood_inundation_plot.png` | Multi-level flood map output |
| `flood_trend_curve.png` | Rising-water trend output |
| `Experiment4_Flood_Inundation.docx` | Original experiment task document |
| `Flood_Inundation_Analysis_Report.docx` | Generated analysis report |
| `report.tex` | Overleaf-ready experiment write-up |

---

## Run It

```bash
# clone and open this project
git clone https://github.com/HuangQiwei123/QiweiHuang-s-homeworks.git
cd QiweiHuang-s-homeworks
git checkout project-4
cd Project-4-Flood-Inundation-Analysis-DEM-based

# install
pip install -r requirements.txt

# reproduce outputs
python generate_dem.py
python visualize_flood.py
python flood_trend.py
python validate_flood.py
```

---

## Development Notes

Built through iterative AI-assisted geospatial analysis:

- Round 1 -- Synthetic DEM generation and basic flood-mask calculation.
- Round 2 -- Multi-level flood extent and depth visualization.
- Round 3 -- Rising-water trend analysis and physical validation suite.

The validation workflow checks 506 physical conditions, including area bounds, non-negative depth, depth-mask consistency, correct maximum depth, and monotonic flooded-area growth.

---

*Huang Qiwei · 3125301141 · Software Development · Xi'an Jiaotong University · 2026*
