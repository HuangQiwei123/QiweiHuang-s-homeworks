# Software Development Course Projects
### Xi'an Jiaotong University · Qiwei Huang · 2026

---

This repository contains four course projects developed for the Software Development class. The topics are connected by one theme: applying Python software development to hydrology and water-resources analysis. Each project includes source code, generated outputs, screenshots, experiment documents, and a project-level README.

The repository is now organized as a clean `main`-branch project archive. The folders are named `project-1` to `project-4` for direct review.

---

## Repository Structure

```text
QiweiHuang-s-homeworks/
|
|-- project-1   -- Rainfall Monitoring and Alert System
|-- project-2   -- SCS-CN Runoff Calculation
|-- project-3   -- Reservoir Dispatch Optimization
`-- project-4   -- DEM-based Flood Inundation Analysis
```

---

## Projects at a Glance

### Project 1 -- Rainfall Monitoring and Alert System
`folder: project-1`

Multi-city rainfall monitoring application for Beijing, Shanghai, Guangzhou, Chengdu, and Wuhan. The program supports OpenWeatherMap real-time data and also provides a simulation mode when no API key is available. It classifies rainfall into Normal / Caution / Alert levels, displays the result with Streamlit and Folium, and stores rainfall history plus alert records.

| | |
|---|---|
| **Python files** | `weather_monitor.py` · `export_map.py` |
| **Output files** | `rainfall_map.html` · `rainfall_history.csv` · `alert_log.txt` |
| **Documents** | `README.md` · `requirements.txt` · `prompt_log.md` · `Experiment1_Rainfall_Alert.docx` |
| **Total files** | 14 files, including `screenshots/` |
| **Dependencies** | `streamlit` · `streamlit-folium` · `folium` · `requests` · `pandas` |

---

### Project 2 -- SCS-CN Runoff Model
`folder: project-2`

Python implementation of the USDA SCS Curve Number method for estimating direct runoff from rainfall. The model focuses on a compact calculation function, boundary-condition testing, and a sensitivity figure that shows how runoff increases with Curve Number.

| | |
|---|---|
| **Python files** | `scs_cn.py` · `test_scs_cn.py` · `sensitivity_analysis.py` |
| **Output files** | `scs_cn_sensitivity.png` |
| **Documents** | `README.md` · `requirements.txt` · `Experiment2_SCSCN_Runoff.docx` |
| **Total files** | 19 files, including `screenshots/` |
| **Dependencies** | `numpy` · `matplotlib` · `pytest` |

---

### Project 3 -- Reservoir Dispatch Optimization
`folder: project-3`

Seven-day reservoir release scheduling model solved with constrained nonlinear optimization. The project calculates hydropower revenue, checks storage and release constraints, and records the final operation plan in both CSV and validation-report formats.

| | |
|---|---|
| **Python files** | `reservoir_optimization.py` |
| **Output files** | `optimal_schedule.csv` · `optimal_schedule_report.txt` · `validation_report.txt` · `tradeoff_analysis.png` |
| **Documents** | `README.md` · `requirements.txt` · `Experiment3_Reservoir_Optimization.docx` |
| **Total files** | 12 files, including `screenshots/` |
| **Dependencies** | `numpy` · `scipy` · `matplotlib` · `pandas` |

---

### Project 4 -- DEM-based Flood Inundation Analysis
`folder: project-4`

DEM-based flood inundation workflow: generate a synthetic 100 x 100 terrain grid, calculate flood masks and depths under different water levels, visualize inundation extent, plot water-level response, and validate the physical consistency of the result.

| | |
|---|---|
| **Python files** | `generate_dem.py` · `flood_inundation.py` · `visualize_flood.py` · `flood_trend.py` · `validate_flood.py` · `write_report.py` |
| **Output files** | `dem_synthetic_100x100.npy` · `dem_synthetic_100x100.csv` · `flood_inundation_plot.png` · `flood_trend_curve.png` · `validation_results.npz` |
| **Documents** | `README.md` · `requirements.txt` · `Experiment4_Flood_Inundation.docx` · `Flood_Inundation_Analysis_Report.docx` |
| **Total files** | 20 files, including `screenshots/` |
| **Dependencies** | `numpy` · `matplotlib` |

---

## Dependencies Summary

| Project | Key Libraries |
|---|---|
| Project 1 | `streamlit` `streamlit-folium` `folium` `requests` `pandas` |
| Project 2 | `numpy` `matplotlib` `pytest` |
| Project 3 | `numpy` `scipy` `matplotlib` `pandas` |
| Project 4 | `numpy` `matplotlib` |

All projects are Python-based and can be reviewed independently from their own folders.

---

## Quick Start

```bash
git clone https://github.com/HuangQiwei123/QiweiHuang-s-homeworks.git
cd QiweiHuang-s-homeworks

python -m venv .venv
.venv\Scripts\activate

pip install -r requirements.txt
```

Run a specific project:

```bash
cd project-1
streamlit run weather_monitor.py

cd ../project-2
python -m pytest test_scs_cn.py -v
python sensitivity_analysis.py

cd ../project-3
python reservoir_optimization.py

cd ../project-4
python generate_dem.py
python flood_inundation.py
python visualize_flood.py
python flood_trend.py
python validate_flood.py
```

---

## Review Route

For grading or review, the recommended order is:

1. Start from this README to understand the four-project structure.
2. Enter each `project-*` folder and read its project-level README.
3. Check the Python files listed in the project table.
4. Inspect generated files such as `.png`, `.csv`, `.html`, `.txt`, and `.docx`.
5. Open `screenshots/` to view the development or interaction process.

---

*Qiwei Huang · Software Development · 2026*
