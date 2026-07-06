# Project 1 -- Rainfall Monitoring and Alert System
### Software Development · Hydrology Application · 2026

---

`folder: project-1`

This project builds a small rainfall warning application for five representative cities in China. It combines weather data collection, rainfall-threshold classification, map visualization, and local record storage. The program can use OpenWeatherMap data when an API key is configured; otherwise it automatically runs with simulated rainfall data for offline demonstration.

---

## Project Details

| | |
|---|---|
| **Python files** | `weather_monitor.py` · `export_map.py` |
| **Output files** | `rainfall_map.html` · `rainfall_history.csv` · `alert_log.txt` |
| **Documents** | `prompt_log.md` · `requirements.txt` · `README.md` · `Experiment1_Rainfall_Alert.docx` |
| **Screenshots** | `screenshots/1.png` · `screenshots/2.png` · `screenshots/3.png` · `screenshots/4.png` · `screenshots/dashboard-page.png` |
| **Dependencies** | `streamlit` · `streamlit-folium` · `folium` · `requests` · `pandas` |

---

## Warning Rule

| Level | Rainfall Intensity | Interpretation |
|---|---:|---|
| Normal | `< 10 mm/h` | ordinary monitoring |
| Caution | `10-20 mm/h` | rainfall deserves attention |
| Alert | `>= 20 mm/h` | heavy rainfall warning |

---

## Main Workflow

```text
weather_monitor.py
  -> fetch or simulate weather data
  -> classify rainfall level
  -> render Streamlit dashboard
  -> record rainfall history and alerts

export_map.py
  -> generate standalone Folium map
  -> save rainfall_map.html
```

---

## Run It

```bash
pip install -r requirements.txt
streamlit run weather_monitor.py
```

Generate the standalone map:

```bash
python export_map.py
```

Optional real-data API key:

```bash
$env:OPENWEATHER_API_KEY="your_api_key"
```

If no API key is set, the simulation mode is used automatically.

---

## Review Notes

- `rainfall_map.html` can be opened directly in a browser.
- `rainfall_history.csv` shows the recorded city-level rainfall data.
- `alert_log.txt` records warning events.
- `screenshots/dashboard-page.png` shows the main dashboard result.
