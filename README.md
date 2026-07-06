# Qiwei Huang - Software Development Course Homeworks

This repository contains four course projects for the Software Development class. The projects are organized around hydrology, water resources, reservoir operation, and flood inundation analysis. Each folder is self-contained and includes source code, generated outputs, screenshots, experiment documents, and a project-level README.

The repository has been reorganized so that the first page of GitHub can be used as a navigation page for review: the teacher can start from this README, enter a project folder, read the project explanation, and run or inspect the corresponding outputs.

## Repository Map

```text
QiweiHuang-s-homeworks/
|-- Project-01-Rainfall-Monitoring-and-Alert/
|   |-- README.md
|   |-- weather_monitor.py
|   |-- export_map.py
|   |-- rainfall_history.csv
|   |-- rainfall_map.html
|   |-- alert_log.txt
|   |-- prompt_log.md
|   |-- screenshots/
|   `-- Experiment1_Rainfall_Alert.docx
|
|-- Project-02-SCS-CN-Runoff-Model/
|   |-- README.md
|   |-- scs_cn.py
|   |-- test_scs_cn.py
|   |-- sensitivity_analysis.py
|   |-- scs_cn_sensitivity.png
|   |-- screenshots/
|   `-- Experiment2_SCSCN_Runoff.docx
|
|-- Project-03-Reservoir-Dispatch-Optimization/
|   |-- README.md
|   |-- reservoir_optimization.py
|   |-- optimal_schedule.csv
|   |-- optimal_schedule_report.txt
|   |-- validation_report.txt
|   |-- tradeoff_analysis.png
|   |-- screenshots/
|   `-- Experiment3_Reservoir_Optimization.docx
|
|-- Project-04-DEM-Flood-Inundation-Analysis/
|   |-- README.md
|   |-- generate_dem.py
|   |-- flood_inundation.py
|   |-- visualize_flood.py
|   |-- flood_trend.py
|   |-- validate_flood.py
|   |-- write_report.py
|   |-- flood_inundation_plot.png
|   |-- flood_trend_curve.png
|   |-- screenshots/
|   `-- Flood_Inundation_Analysis_Report.docx
|
|-- requirements.txt
|-- .gitignore
`-- README.md
```

## Project Summary

| Project | Topic | Main Method | Main Deliverables |
|---|---|---|---|
| Project 01 | Rainfall monitoring and warning | Streamlit dashboard, Folium map, OpenWeatherMap or simulated rainfall data | Interactive dashboard, HTML map, rainfall history, alert log |
| Project 02 | SCS-CN runoff calculation | USDA SCS Curve Number equation, pytest validation, sensitivity plotting | Runoff model, 39 unit tests, sensitivity figure |
| Project 03 | Reservoir dispatch optimization | Constrained nonlinear optimization with `scipy.optimize` | 7-day schedule, validation report, trade-off analysis |
| Project 04 | DEM flood inundation analysis | Synthetic DEM, water-level inundation mask, depth calculation, monotonicity validation | DEM data, flood maps, trend curve, validation data |

## Quick Setup

```bash
git clone https://github.com/HuangQiwei123/QiweiHuang-s-homeworks.git
cd QiweiHuang-s-homeworks

python -m venv .venv

# Windows PowerShell
.venv\Scripts\activate

# macOS/Linux
# source .venv/bin/activate

pip install -r requirements.txt
```

If a single project is being reviewed, it is also possible to enter that project folder and install its own `requirements.txt`.

## Project 01 - Rainfall Monitoring and Alert

This project builds a small rainfall warning application for five Chinese cities: Beijing, Shanghai, Guangzhou, Chengdu, and Wuhan. It can call OpenWeatherMap when an API key is available. If no key is provided, the program switches to simulated rainfall data, so the dashboard can still be demonstrated offline.

Main functions:

- collect rainfall, temperature, humidity, location, and timestamp data;
- classify rainfall into normal, caution, and alert levels;
- display city status on a Streamlit dashboard and a Folium map;
- export an HTML map for direct browser viewing;
- save rainfall history and alert events to local files.

Run:

```bash
cd Project-01-Rainfall-Monitoring-and-Alert
pip install -r requirements.txt
streamlit run weather_monitor.py
python export_map.py
```

Review outputs:

- `rainfall_map.html` shows the generated map;
- `rainfall_history.csv` stores monitoring records;
- `alert_log.txt` stores alert events;
- `screenshots/` contains page and interaction screenshots.

## Project 02 - SCS-CN Runoff Model

This project implements the SCS Curve Number method for direct runoff estimation. It focuses on a clear model function, boundary-condition tests, and visual sensitivity analysis.

Model equations:

```text
S  = 25400 / CN - 254
Ia = 0.2 * S

Q = 0,                         if P <= Ia
Q = (P - Ia)^2 / (P - Ia + S), if P > Ia
```

Run:

```bash
cd Project-02-SCS-CN-Runoff-Model
pip install -r requirements.txt
python -m pytest test_scs_cn.py -v
python sensitivity_analysis.py
```

Review outputs:

- `test_scs_cn.py` contains 39 test cases;
- `scs_cn_sensitivity.png` visualizes the nonlinear relation between CN and runoff;
- `Experiment2_SCSCN_Runoff.docx` contains the written experiment document.

## Project 03 - Reservoir Dispatch Optimization

This project formulates a 7-day reservoir operation problem. The decision variable is daily release. The objective is to improve hydropower revenue while satisfying physical and environmental constraints.

Main constraints:

- storage must stay between minimum and maximum capacity;
- release must stay within operation limits;
- ecological release requirement must be satisfied;
- daily mass balance must remain valid.

Run:

```bash
cd Project-03-Reservoir-Dispatch-Optimization
pip install -r requirements.txt
python reservoir_optimization.py
```

Review outputs:

- `optimal_schedule.csv` gives the 7-day release and storage plan;
- `optimal_schedule_report.txt` summarizes the optimization result;
- `validation_report.txt` checks feasibility;
- `tradeoff_analysis.png` shows the relationship between revenue and ecological objectives.

## Project 04 - DEM Flood Inundation Analysis

This project creates a synthetic 100 x 100 DEM and analyzes flood inundation under different water levels. It calculates flooded cells, water depth, flooded area percentage, and water-level response trends.

Workflow:

```text
generate_dem.py       -> create DEM data
flood_inundation.py   -> calculate mask, depth, area, volume
visualize_flood.py    -> generate inundation figure
flood_trend.py        -> plot water level versus flooded area
validate_flood.py     -> run physical-sense checks
write_report.py       -> prepare report document
```

Run:

```bash
cd Project-04-DEM-Flood-Inundation-Analysis
pip install -r requirements.txt
python generate_dem.py
python flood_inundation.py
python visualize_flood.py
python flood_trend.py
python validate_flood.py
```

Review outputs:

- `dem_synthetic_100x100.csv` and `dem_synthetic_100x100.npy` store DEM data;
- `flood_inundation_plot.png` shows DEM, flood extent, and depth;
- `flood_trend_curve.png` shows the water-level response;
- `validation_results.npz` stores validation arrays.

## Review Guide

For a quick review, open the folders in order:

1. Read each project-level `README.md`.
2. Check the Python files listed in the README.
3. Inspect generated result files such as `.png`, `.csv`, `.html`, and `.txt`.
4. Open `screenshots/` to see the interaction or running process.
5. Open the `.docx` report when a formal write-up is needed.

## Notes

- The source code and output files are kept in their original project folders.
- Generated Python cache files have been removed from version control.
- Local virtual environments, temporary files, and private API keys are excluded by `.gitignore`.
- Project READMEs are written as independent entry points so each experiment can be reviewed separately.
