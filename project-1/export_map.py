"""Standalone: generate Folium rainfall map as HTML (no Streamlit needed)."""
import random
import time
from datetime import datetime

import folium

CITIES = {
    "Beijing":   ("北京", 39.91, 116.40),
    "Shanghai":  ("上海", 31.23, 121.47),
    "Guangzhou": ("广州", 23.13, 113.26),
    "Chengdu":   ("成都", 30.57, 104.07),
    "Wuhan":     ("武汉", 30.59, 114.31),
}

WARNING_LEVELS = {
    "green":  {"color": "#4CAF50"},
    "yellow": {"color": "#FF9800"},
    "red":    {"color": "#F44336"},
}

CHINA_CENTER = (35.86, 104.19)
DEFAULT_ZOOM = 4


def classify_rainfall(mmh: float) -> str:
    if mmh < 10:
        return "green"
    if mmh < 20:
        return "yellow"
    return "red"


def simulate(city_en: str, lat: float) -> dict:
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
        "rainfall_mmh": min(rain, 50),
        "temp": round(15 + 25 * rng.random(), 1),
        "humidity": rng.randint(40, 95),
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


def build_map() -> folium.Map:
    m = folium.Map(location=CHINA_CENTER, zoom_start=DEFAULT_ZOOM, tiles="OpenStreetMap")

    for city_en, (city_cn, lat, lon) in CITIES.items():
        data = simulate(city_en, lat)
        level = classify_rainfall(data["rainfall_mmh"])
        folium_color = {"green": "green", "yellow": "orange", "red": "red"}[level]

        popup_html = f"""
        <div style="font-family: sans-serif; min-width: 170px;">
            <b style="font-size: 16px;">{city_cn}</b> <small>({city_en})</small><br>
            <hr style="margin: 6px 0;">
            Rainfall: <b>{data['rainfall_mmh']:.1f} mm/h</b><br>
            Status: <span style="color:{WARNING_LEVELS[level]['color']}; font-weight:bold;">
                {level.upper()}
            </span><br>
            <small>🌡 {data['temp']}°C  |  💧 {data['humidity']}%</small><br>
            <small>{data['timestamp']}</small>
        </div>
        """

        folium.Marker(
            location=[lat, lon],
            popup=folium.Popup(popup_html, max_width=250),
            icon=folium.Icon(color=folium_color, icon="cloud-rain", prefix="fa"),
            tooltip=f"{city_cn} — {data['rainfall_mmh']:.1f} mm/h",
        ).add_to(m)

    folium.LayerControl().add_to(m)
    return m


if __name__ == "__main__":
    m = build_map()
    output = "rainfall_map.html"
    m.save(output)
    print(f"Map saved to {output}")
