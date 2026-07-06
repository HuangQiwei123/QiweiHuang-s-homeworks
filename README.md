# Software Development -- Specialized Experiments

**Xi'an Jiaotong University · Huang Qiwei · 2026**

Four water-related engineering experiments built end-to-end with AI-assisted software development. Each project follows the same workflow: structured prompting, AI-generated code, iterative refinement, physical validation, and documented outputs.

---

## Repository Structure

```text
QiweiHuang-s-homeworks/
├── Project-1-Short-term-Rainfall-Forecasting-and-Alert-System
│   └── Rainfall monitoring dashboard and warning logic
├── Project-2-Hydrological-Modeling-SCS-CN-Runoff
│   └── SCS-CN runoff calculation and sensitivity analysis
├── Project-3-Water-Resources-Optimization-Reservoir-Dispatch
│   └── Reservoir dispatch optimization and trade-off analysis
└── Project-4-Flood-Inundation-Analysis-DEM-based
    └── DEM-based flood simulation, visualization, and validation
```

---

## Projects at a Glance

### Project 1 -- Rainfall Forecasting and Alert System

`branch: project-1`

Real-time rainfall monitoring using OpenWeatherMap data or simulation mode. The system classifies rainfall into Normal / Caution / Alert levels, logs red alerts, and displays current conditions through a multi-city Streamlit dashboard with a Folium map.

| Category | Files |
| --- | --- |
| Python files | `weather_monitor.py` · `export_map.py` |
| Output files | `alert_log.txt` · `rainfall_history.csv` · `rainfall_map.html` |
| Docs | `Experiment1_Rainfall_Alert.docx` · `prompt_log.md` · `report.tex` · `README.md` |
| Screenshots | `screenshots/1.png` · `screenshots/2.png` · `screenshots/3.png` · `screenshots/4.png` · `screenshots/dashboard-page.png` |
| Dependencies | `streamlit` · `streamlit-folium` · `folium` · `requests` · `pandas` |

[Open Project 1](Project-1-Short-term-Rainfall-Forecasting-and-Alert-System/)

---

### Project 2 -- SCS-CN Runoff Model

`branch: project-2`

Python implementation of the USDA Soil Conservation Service Curve Number method for estimating direct runoff from rainfall. The model includes boundary-condition tests, vectorized NumPy support, and sensitivity analysis across CN values.

| Category | Files |
| --- | --- |
| Python files | `scs_cn.py` · `test_scs_cn.py` · `sensitivity_analysis.py` |
| Output files | `scs_cn_sensitivity.png` |
| Docs | `Experiment2_SCSCN_Runoff.docx` · `report.tex` · `README.md` |
| Screenshots | `screenshots/1.png` · `screenshots/2.png` · `screenshots/3.png` · `screenshots/4.png` · `screenshots/5.png` |
| Dependencies | `numpy` · `matplotlib` · `pillow` · `pytest` |

[Open Project 2](Project-2-Hydrological-Modeling-SCS-CN-Runoff/)

---

### Project 3 -- Reservoir Dispatch Optimization

`branch: project-3`

Seven-day reservoir release optimization with hydropower revenue, ecological release, storage bounds, and mass-balance constraints. The workflow exports an optimal schedule, validates all physical constraints, and visualizes the revenue-ecology trade-off.

| Category | Files |
| --- | --- |
| Python files | `reservoir_optimization.py` |
| Output files | `optimal_schedule.csv` · `optimal_schedule_report.txt` · `validation_report.txt` · `tradeoff_analysis.png` |
| Docs | `Experiment3_Reservoir_Optimization.docx` · `report.tex` · `README.md` |
| Screenshots | `screenshots/1.png` · `screenshots/2.png` · `screenshots/3.png` · `screenshots/4.png` |
| Dependencies | `numpy` · `scipy` · `matplotlib` · `pillow` |

[Open Project 3](Project-3-Water-Resources-Optimization-Reservoir-Dispatch/)

---

### Project 4 -- Flood Inundation Analysis (DEM-based)

`branch: project-4`

DEM-based flood inundation analysis using a synthetic 100 x 100 terrain grid. The pipeline covers DEM generation, flood-mask calculation, depth and volume metrics, multi-level visualization, rising-water trend analysis, and physical-sense validation.

| Category | Files |
| --- | --- |
| Python files | `generate_dem.py` · `flood_inundation.py` · `visualize_flood.py` · `flood_trend.py` · `validate_flood.py` · `write_report.py` |
| Output files | `dem_synthetic_100x100.npy` · `dem_synthetic_100x100.csv` · `flood_inundation_plot.png` · `flood_trend_curve.png` · `validation_results.npz` |
| Docs | `Experiment4_Flood_Inundation.docx` · `Flood_Inundation_Analysis_Report.docx` · `report.tex` · `README.md` |
| Screenshots | `screenshots/1.png` · `screenshots/2.png` · `screenshots/3.png` · `screenshots/4.png` · `screenshots/5.png` |
| Dependencies | `numpy` · `matplotlib` · `pillow` · `python-docx` |

[Open Project 4](Project-4-Flood-Inundation-Analysis-DEM-based/)

---

## Dependencies Summary

| Project | Key Libraries |
| --- | --- |
| Project 1 | `streamlit` · `requests` · `pandas` · `folium` |
| Project 2 | `numpy` · `matplotlib` · `pillow` · `pytest` |
| Project 3 | `numpy` · `scipy` · `matplotlib` · `pillow` |
| Project 4 | `numpy` · `matplotlib` · `pillow` · `python-docx` |

All projects target Python 3.10+ and are self-contained with their own `requirements.txt`.

---

## Clone and Switch

```bash
git clone https://github.com/HuangQiwei123/QiweiHuang-s-homeworks.git
cd QiweiHuang-s-homeworks

git checkout main       # full portfolio
git checkout project-1  # Rainfall alert system
git checkout project-2  # SCS-CN runoff model
git checkout project-3  # Reservoir optimization
git checkout project-4  # Flood inundation analysis
```

Each project directory contains a `README.md` with setup and run instructions specific to that experiment.

---

*Huang Qiwei · Software Development · 2026*
