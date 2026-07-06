# Rainfall Forecasting & Alert System

**Specialized Experiment 1 · Xi'an Jiaotong University · Software Development 2026**

Real-time rainfall monitoring powered by the OpenWeatherMap API and Streamlit. The dashboard fetches or simulates live weather data, classifies rainfall intensity into three severity levels, logs every red alert, and renders current conditions in a multi-city interactive map.

---

## Alert Classification

| Severity | Threshold | Indicator |
| --- | --- | --- |
| Normal | `< 10 mm/h` | Green · no action |
| Caution | `10-20 mm/h` | Yellow · elevated monitoring |
| Heavy Rainfall | `>= 20 mm/h` | Red · flood-risk alert |

---

## What's Inside

| File | Role |
| --- | --- |
| `weather_monitor.py` | Streamlit dashboard; fetches rainfall, temperature, humidity, timestamp, and alert level |
| `export_map.py` | Exports the Folium rainfall map to `rainfall_map.html` |
| `alert_log.txt` | Timestamped history of triggered heavy-rainfall alerts |
| `rainfall_history.csv` | Sample monitoring history for the dashboard table |
| `rainfall_map.html` | Static exported map artifact |
| `prompt_log.md` | Record of AI prompts and development iterations |
| `Experiment1_Rainfall_Alert.docx` | Original experiment task document |
| `report.tex` | Overleaf-ready experiment write-up |
| `requirements.txt` | Python dependencies |

---

## Run It

```bash
# clone and open this project
git clone https://github.com/HuangQiwei123/QiweiHuang-s-homeworks.git
cd QiweiHuang-s-homeworks
git checkout project-1
cd Project-1-Short-term-Rainfall-Forecasting-and-Alert-System

# install
pip install -r requirements.txt

# launch
# optional: set OPENWEATHER_API_KEY for live data
streamlit run weather_monitor.py
```

---

## Development Notes

Built through iterative AI-assisted development:

- Round 1 -- API integration, rainfall parsing, and error handling.
- Round 2 -- Threshold classification, alert logging, and physical-unit validation.
- Round 3 -- Streamlit dashboard, Folium map, history table, and auto-refresh support.

The app can run without an API key by switching to deterministic simulation mode, which makes the project easy to review in a classroom environment.

---

*Huang Qiwei · 3125301141 · Software Development · Xi'an Jiaotong University · 2026*
