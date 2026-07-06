# Project 01 - Rainfall Monitoring and Alert

## Overview

This project implements a rainfall monitoring and warning prototype for selected Chinese cities. The application combines weather data acquisition, threshold-based warning logic, map visualization, and simple log persistence.

The project can run in two modes:

- Real-data mode: use an OpenWeatherMap API key to request current weather information.
- Simulation mode: if no API key is configured, generate stable simulated rainfall values so the dashboard can still be tested and demonstrated.

## Objectives

- Build a small but complete rainfall warning workflow.
- Display rainfall conditions on an interactive dashboard.
- Provide a map-based view of city rainfall status.
- Record rainfall history and alert events.
- Keep the experiment reproducible even without an external API key.

## Warning Logic

| Level | Rainfall Range | Meaning |
|---|---:|---|
| Normal | `< 10 mm/h` | Normal monitoring |
| Caution | `10-20 mm/h` | Increased attention |
| Alert | `>= 20 mm/h` | Strong rainfall warning |

## File Description

| File or Folder | Purpose |
|---|---|
| `weather_monitor.py` | Main Streamlit application. It fetches or simulates weather data, classifies rainfall, displays charts and map markers, and writes records. |
| `export_map.py` | Standalone Folium script for generating `rainfall_map.html` without launching Streamlit. |
| `rainfall_history.csv` | Historical rainfall records generated during monitoring. |
| `alert_log.txt` | Alert log for heavy rainfall events. |
| `rainfall_map.html` | Browser-readable map output. |
| `prompt_log.md` | AI-assisted development record. |
| `screenshots/` | Dashboard and interaction screenshots. |
| `Experiment1_Rainfall_Alert.docx` | Experiment report. |
| `requirements.txt` | Dependencies for this project. |

## How to Run

```bash
cd Project-01-Rainfall-Monitoring-and-Alert
pip install -r requirements.txt
streamlit run weather_monitor.py
```

Generate the standalone map:

```bash
python export_map.py
```

## API Key Configuration

Real weather data requires OpenWeatherMap:

```bash
# Windows PowerShell
$env:OPENWEATHER_API_KEY="your_api_key"

# macOS/Linux
export OPENWEATHER_API_KEY="your_api_key"
```

If the key is not configured, the program automatically uses simulation mode.

## Results to Inspect

- `rainfall_map.html`: city rainfall status on a map.
- `rainfall_history.csv`: saved monitoring records.
- `alert_log.txt`: alert output when rainfall exceeds the threshold.
- `screenshots/dashboard-page.png`: dashboard page screenshot.

## Development Notes

The experiment demonstrates a complete software workflow rather than only a formula calculation: data input, decision logic, visualization, file output, and user interaction are all included.
