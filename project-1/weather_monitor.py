"""
Rainfall Monitor - National View
Multi-city real-time rainfall monitoring with Folium map and threshold-based alerting.
"""
import os
import random
import time
from datetime import datetime
from pathlib import Path
from typing import Any

import folium
import pandas as pd
import requests
import streamlit as st
from streamlit_folium import st_folium

# ── Page config ────────────────────────────────────────────────────────────

st.set_page_config(
    page_title="Rainfall Monitor - National View",
    page_icon="🌧️",
    layout="wide",
)

# ── Paths ──────────────────────────────────────────────────────────────────

BASE_DIR = Path(__file__).resolve().parent
LOG_FILE = BASE_DIR / "alert_log.txt"
DATA_FILE = BASE_DIR / "rainfall_history.csv"

# ── Constants ──────────────────────────────────────────────────────────────

CITIES: dict[str, tuple[str, float, float]] = {
    "Beijing":   ("北京", 39.91, 116.40),
    "Shanghai":  ("上海", 31.23, 121.47),
    "Guangzhou": ("广州", 23.13, 113.26),
    "Chengdu":   ("成都", 30.57, 104.07),
    "Wuhan":     ("武汉", 30.59, 114.31),
}

WARNING_LEVELS = {
    "green":  {"label": "Normal",       "color": "#4CAF50", "icon": "🟢", "threshold": 10},
    "yellow": {"label": "Caution",      "color": "#FF9800", "icon": "🟡", "threshold": 20},
    "red":    {"label": "Alert",        "color": "#F44336", "icon": "🔴", "threshold": float("inf")},
}

ALERT_THRESHOLD = 20  # mm/h — triggers alert banner & log

CHINA_CENTER = (35.86, 104.19)
DEFAULT_ZOOM = 4

REQUEST_TIMEOUT = 10

# ── API key ────────────────────────────────────────────────────────────────


def get_api_key() -> str:
    try:
        return st.secrets.get("OPENWEATHER_API_KEY", "")
    except Exception:
        return os.environ.get("OPENWEATHER_API_KEY", "")


API_KEY = get_api_key()
USE_SIMULATION = not API_KEY

# ── Warning classifier ─────────────────────────────────────────────────────


def classify_rainfall(mmh: float) -> dict[str, Any]:
    if mmh < 10:
        level = "green"
    elif mmh < 20:
        level = "yellow"
    else:
        level = "red"
    cfg = WARNING_LEVELS[level]
    return {"level": level, "label": cfg["label"], "color": cfg["color"], "icon": cfg["icon"]}


# ── Data fetching ──────────────────────────────────────────────────────────


def fetch_weather(city_en: str, lat: float, lon: float) -> dict[str, Any]:
    """Fetch live weather from OpenWeatherMap, or use simulation."""
    if USE_SIMULATION:
        return _simulate_weather(city_en, lat, lon)

    try:
        params = {"lat": lat, "lon": lon, "appid": API_KEY, "units": "metric"}
        resp = requests.get("https://api.openweathermap.org/data/2.5/weather",
                            params=params, timeout=REQUEST_TIMEOUT)
        resp.raise_for_status()
        data = resp.json()

        rain_mmh = 0.0
        rain_block = data.get("rain", {})
        if isinstance(rain_block, dict):
            rain_mmh = rain_block.get("1h", rain_block.get("3h", 0.0))

        return {
            "city_en": city_en,
            "temp": data["main"]["temp"],
            "humidity": data["main"]["humidity"],
            "rainfall_mmh": round(rain_mmh, 2),
            "weather_desc": data["weather"][0]["description"],
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "lat": lat,
            "lon": lon,
            "error": None,
        }
    except requests.RequestException as exc:
        return {
            "city_en": city_en,
            "temp": 0, "humidity": 0, "rainfall_mmh": 0,
            "weather_desc": "N/A",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "lat": lat, "lon": lon,
            "error": str(exc),
        }


def _simulate_weather(city_en: str, lat: float, lon: float) -> dict[str, Any]:
    """Simulate rainfall based on latitude — north drier, south wetter."""
    seed = int(time.time() / 300) + hash(city_en) % 1000
    rng = random.Random(seed)

    if lat > 38:
        rain = round(rng.expovariate(1 / 2.0), 2)
    elif lat > 28:
        rain = round(rng.expovariate(1 / 6.0), 2)
    else:
        rain = round(rng.expovariate(1 / 10.0), 2)

    return {
        "city_en": city_en,
        "temp": round(15 + 25 * rng.random(), 1),
        "humidity": rng.randint(40, 95),
        "rainfall_mmh": min(rain, 50),
        "weather_desc": "Simulated data",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "lat": lat,
        "lon": lon,
        "error": None,
    }


# ── Persistence ────────────────────────────────────────────────────────────


def log_alert(city_cn: str, rainfall: float, level: str) -> None:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    entry = f"[{timestamp}] {level.upper()} | {city_cn} | {rainfall:.1f} mm/h\n"
    with open(LOG_FILE, "a", encoding="utf-8") as f:
        f.write(entry)


def save_to_history(records: list[dict]) -> None:
    df_new = pd.DataFrame(records)
    if DATA_FILE.exists():
        df_old = pd.read_csv(DATA_FILE)
        df_all = pd.concat([df_old, df_new], ignore_index=True)
    else:
        df_all = df_new
    df_all.to_csv(DATA_FILE, index=False)


def load_history() -> pd.DataFrame:
    if DATA_FILE.exists():
        return pd.read_csv(DATA_FILE)
    return pd.DataFrame(columns=["city_en", "city_cn", "rainfall_mmh", "level", "timestamp"])


# ── Map builder ────────────────────────────────────────────────────────────


def build_map(records: list[dict]) -> folium.Map:
    m = folium.Map(location=CHINA_CENTER, zoom_start=DEFAULT_ZOOM, tiles="OpenStreetMap")

    for r in records:
        folium_color = "green" if r["level"] == "green" else "orange" if r["level"] == "yellow" else "red"
        popup_html = f"""
        <div style="font-family: sans-serif; min-width: 160px;">
            <b style="font-size: 16px;">{r['city_cn']}</b> <small>({r['city_en']})</small><br>
            <hr style="margin: 6px 0;">
            Rainfall: <b>{r['rainfall_mmh']:.1f} mm/h</b><br>
            Status: <span style="color:{WARNING_LEVELS[r['level']]['color']}; font-weight:bold;">
                {r['level'].upper()}
            </span><br>
            <small>🌡 {r['temp']}°C  |  💧 {r['humidity']}%</small>
        </div>
        """

        folium.Marker(
            location=[r["lat"], r["lon"]],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=folium_color, icon="cloud-rain", prefix="fa"),
            tooltip=f"{r['city_cn']} — {r['rainfall_mmh']:.1f} mm/h",
        ).add_to(m)

    folium.LayerControl().add_to(m)
    return m


# ── Dashboard ──────────────────────────────────────────────────────────────


def main() -> None:
    st.title("🌧️ Rainfall Monitor — National View")
    st.caption(
        f"Five-city real-time monitoring  |  "
        f"{'🔶 Simulation Mode' if USE_SIMULATION else '🟢 Live API Mode'}"
    )

    # ── Top bar: refresh button + last-updated timestamp ─────────────
    top_left, top_right = st.columns([1, 3])
    with top_left:
        if st.button("🔄 Refresh Data", use_container_width=True, type="primary"):
            st.session_state.pop("cached_records", None)
            st.session_state.pop("cached_alerts", None)
            st.session_state.next_refresh_at = 0
            st.rerun()
    with top_right:
        if "last_fetch_time" in st.session_state:
            st.markdown(
                f"<div style='padding:8px 0; color:#666; font-size:14px;'>"
                f"📅 Last updated: <b>{st.session_state.last_fetch_time}</b>"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── Sidebar ────────────────────────────────────────────────────────
    with st.sidebar:
        st.header("⚙️ Settings")
        show_alerts = st.checkbox("Show alert log", value=True)
        show_history_table = st.checkbox("Show recent history", value=False)
        st.divider()
        st.caption(f"Alert threshold: **≥ {ALERT_THRESHOLD} mm/h** (Red)")
        st.caption(
            f"{'🔶 Simulation Mode' if USE_SIMULATION else '🟢 Live API Mode'}"
        )

    # ── Determine whether to fetch ─────────────────────────────────────
    now = time.time()
    if "next_refresh_at" not in st.session_state:
        st.session_state.next_refresh_at = 0

    if now >= st.session_state.next_refresh_at:
        with st.spinner("Fetching current rainfall data..."):
            records: list[dict] = []
            alerts: list[dict] = []

            for city_en, (city_cn, lat, lon) in CITIES.items():
                data = fetch_weather(city_en, lat, lon)
                cls = classify_rainfall(data["rainfall_mmh"])
                data["city_cn"] = city_cn
                data.update(cls)
                records.append(data)

                if data["rainfall_mmh"] >= ALERT_THRESHOLD:
                    alerts.append(data)
                    log_alert(city_cn, data["rainfall_mmh"], cls["level"])

            st.session_state.cached_records = records
            st.session_state.cached_alerts = alerts
            st.session_state.last_fetch_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            st.session_state.next_refresh_at = float("inf")  # don't re-fetch until button clicked

            try:
                save_to_history(records)
            except Exception:
                pass
    else:
        records = st.session_state.cached_records
        alerts = st.session_state.cached_alerts

    # ── Alert banner ───────────────────────────────────────────────────
    if alerts:
        names = ", ".join(r["city_cn"] for r in alerts)
        st.error(f"🚨 ALERT: Heavy rainfall detected — **{names}**")
    else:
        st.success("✅ All cities below alert threshold.")

    # ── Folium map ─────────────────────────────────────────────────────
    st.subheader("🗺️ National Rainfall Map")
    m = build_map(records)
    st_folium(m, width="100%", height=500, key="rainfall_map")

    # ── Legend ─────────────────────────────────────────────────────────
    st.caption("")  # spacer
    legend_cols = st.columns(3)
    for col, (level, cfg) in zip(legend_cols, WARNING_LEVELS.items()):
        with col:
            st.markdown(
                f"<div style='background:{cfg['color']}18; border-left:4px solid {cfg['color']}; "
                f"padding:6px 12px; border-radius:4px; font-size:14px;'>"
                f"{cfg['icon']} <b>{level.upper()}</b> — {cfg['label']} "
                f"({'<' if level == 'green' else '≥' if level == 'red' else ''}{cfg['threshold']} mm/h)"
                f"</div>",
                unsafe_allow_html=True,
            )

    # ── City cards ─────────────────────────────────────────────────────
    st.subheader("📊 Current Rainfall")
    cols = st.columns(len(records))

    for col, r in zip(cols, records):
        bg = r["color"]
        with col:
            st.markdown(f"""
            <div style="
                background: {bg}15;
                border: 2px solid {bg};
                border-radius: 12px;
                padding: 14px 8px;
                text-align: center;
                height: 100%;
            ">
                <div style="font-size: 20px; font-weight: bold;">{r['icon']} {r['city_cn']}</div>
                <div style="font-size: 36px; font-weight: bold; color: {bg}; margin: 6px 0;">
                    {r['rainfall_mmh']:.1f}
                </div>
                <div style="font-size: 13px; color: #888;">mm/h</div>
                <div style="
                    display: inline-block;
                    background: {bg};
                    color: white;
                    padding: 3px 14px;
                    border-radius: 20px;
                    font-size: 13px;
                    font-weight: 600;
                    margin-top: 6px;
                ">{r['label']}</div>
                <div style="font-size: 11px; color: #999; margin-top: 6px;">
                    🌡 {r['temp']}°C  |  💧 {r['humidity']}%
                </div>
            </div>
            """, unsafe_allow_html=True)

    # ── Data table ─────────────────────────────────────────────────────
    st.divider()
    st.subheader("📋 Data Table")

    df = pd.DataFrame(records)
    df_display = df[["city_cn", "rainfall_mmh", "level", "temp", "humidity", "weather_desc", "timestamp"]]
    df_display.columns = ["City", "Rainfall (mm/h)", "Level", "Temp (°C)", "Humidity (%)", "Weather", "Timestamp"]

    def row_style(row: pd.Series) -> list[str]:
        level = row.get("Level", "green")
        color = WARNING_LEVELS.get(level, WARNING_LEVELS["green"])["color"]
        return [f"background-color: {color}18" for _ in row]

    styled = df_display.style.apply(row_style, axis=1).format({"Rainfall (mm/h)": "{:.1f}"})
    st.dataframe(styled, use_container_width=True, hide_index=True)

    # ── History (optional) ─────────────────────────────────────────────
    if show_history_table:
        st.divider()
        st.subheader("📜 Recent History (last 25 records)")
        df_hist = load_history()
        if not df_hist.empty:
            st.dataframe(df_hist.tail(25), use_container_width=True, hide_index=True)
        else:
            st.info("No historical data yet.")

    # ── Alert log ──────────────────────────────────────────────────────
    if show_alerts:
        st.divider()
        st.subheader("🚨 Alert Log")
        if LOG_FILE.exists():
            with open(LOG_FILE, "r", encoding="utf-8") as f:
                lines = f.readlines()
            if lines:
                st.code("".join(lines[-20:][::-1]), language="text")
            else:
                st.info("No alerts triggered yet.")
        else:
            st.info("No alerts triggered yet.")

    # ── Refresh footer ─────────────────────────────────────────────────
    st.caption(
        f"💡 Click the **🔄 Refresh Data** button at the top to fetch new data.  |  "
        f"{'🔶 Simulated' if USE_SIMULATION else '🟢 Live data'}"
    )


if __name__ == "__main__":
    main()
