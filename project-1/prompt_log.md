# Prompt Log — Experiment 1: Short-term Rainfall Forecasting & Alert System

## AI-Assisted Development Documentation

**Student:** 黄琦伟 (3125301141)
**Date:** 2026-05-09
**Course:** Smart Water Lab Series — Week 5, Session A

---

### Prompt 1: Initial System Design

**Prompt:**
> I am a water resources student building a rainfall monitoring system. I need a Streamlit dashboard that monitors multiple Chinese cities (not just Beijing). The dashboard should:
> 1. Fetch current weather data via OpenWeatherMap API for 8+ cities
> 2. Classify rainfall using CMA standards (Light/Moderate/Heavy/Violent)
> 3. Display color-coded alert cards for each city
> 4. Show comparison bar charts and historical trend lines
> 5. Log alerts to file with timestamps
> 6. Include a fallback simulation mode when no API key is available
> 7. Auto-refresh at configurable intervals

**AI Response Summary:** Generated `weather_monitor.py` with 12 Chinese cities, CMA rainfall classification, Streamlit wide-layout dashboard, matplotlib charts, and CSV-based historical tracking.

**Corrections Made:**
- Fixed `st.secrets` access to handle missing secrets.toml gracefully
- Adjusted rainfall category thresholds to match CMA standard exactly

---

### Prompt 2: Multi-City Expansion

**Prompt:**
> The original template only used Beijing. Please add 11 more major Chinese cities covering different climate zones (north/central/south) so the dashboard shows diverse rainfall patterns.

**AI Response Summary:** Added Shanghai, Guangzhou, Shenzhen, Chengdu, Wuhan, Xi'an, Nanjing, Hangzhou, Chongqing, Harbin, and Kunming — covering temperate, subtropical, and plateau climate zones with different baseline rainfall characteristics.

---

### Prompt 3: UI Richness

**Prompt:**
> The dashboard feels basic. Make it richer:
> - City cards with colored borders matching alert levels
> - Large rainfall numbers
> - Temperature and humidity on each card
> - Better alert banner at the top
> - Map showing monitored cities

**AI Response Summary:** Redesigned city cards with CSS-styled containers, color-matched borders, large typography for rainfall values, and added a Streamlit map component showing all monitored cities.

---

### Validation Notes

| Check | Result |
|-------|--------|
| Classification accuracy (0.5/3.0/10.0/20.0 mm/h) | ✅ Correct |
| Simulation generates latitude-aware rainfall | ✅ North drier, south wetter |
| Alert threshold (16 mm/h) triggers correctly | ✅ Verified |
| CSV history appends correctly | ✅ Verified |
| Multiple cities render in dashboard | ✅ Verified |

---

---

### Prompt 4: Multi-City Refactor & Folium Map

**Prompt:**
> 将单城市扩展为多城市监控。5 个中国城市（北京、上海、广州、成都、武汉），使用 OpenWeatherMap API 获取数据，提取城市名、经纬度、降雨强度。预警逻辑：<10 mm/h 绿色，10–20 mm/h 黄色，>=20 mm/h 红色。用 Folium + streamlit_folium 绘制带彩色 Marker 的地图，Popup 显示城市名和降雨量。5 分钟自动刷新。

**AI Response Summary:** Rewrote `weather_monitor.py`: reduced from 12 cities to 5, simplified from 4 CMA categories to 3-level warning system (green/yellow/red), replaced `st.map()` with Folium markers colored by alert level using `streamlit_folium`, removed matplotlib bar/history charts to keep dashboard focused. Auto-refresh via `st.session_state` timer + `st.rerun()` loop without extra dependencies. Retained simulation mode, alert logging, CSV history, and sidebar controls.

**Corrections Made:**
- Switched from 4-tier CMA classification to simple 3-level threshold system per updated brief
- Used `folium.Icon(color=...)` with `prefix="fa"` for Font Awesome cloud-rain icons
- Simulation `expovariate` lambda values re-tuned for 5-city latitude bands
- Kept `st.session_state` caching so data is only re-fetched on interval expiry, not every re-render

---

### Prompt 5: Interaction Polish & File Cleanup

**Prompt:**
> 更新桌面 Experiment1_Rainfall_Alert 目录中的文件，删去 C:\Users\hqw 下的冲突重复文件，交互过程进行适当完善但不多余。

**AI Response Summary:** Deleted `multi_city_rainfall_monitor.py` and `weather_monitor.py` from `C:\Users\hqw\`. Improved dashboard interaction: legend below map explains color thresholds inline, city cards use colored pills for status labels, alert log shows most recent 20 entries reversed, optional history table behind sidebar checkbox, countdown timer shows seconds until next fetch.

---

### Key Learnings

1. OpenWeatherMap free tier has rate limits (60 calls/min) — simulation mode avoids this during development
2. CMA rainfall categories differ from the simplified 3-level threshold system now required
3. `folium.Icon(color=...)` supports `green`/`orange`/`red` natively; yellow markers are illegible on map tiles
4. `st.session_state` caching decouples fetch frequency from UI re-render frequency, keeping the dashboard responsive while respecting API rate limits
5. Separating API fetch logic from display logic makes testing easier
6. `streamlit_folium` requires `pip install streamlit-folium` — adds one dependency beyond base Streamlit

---

### Prompt 6: Crash Fix & Browser-Side Auto-Refresh

**Prompt:**
> 打开之后就卡退

**AI Response Summary:** Diagnosed root cause: `time.sleep(2); st.rerun()` at the bottom of `main()` created a server-side busy loop that re-executed the entire script every 2 seconds. On WebSocket disconnect this caused immediate crash. Replaced with `st.components.v1.html()` injecting a JavaScript `setTimeout` that triggers `window.location.reload()` after the configured interval — refresh happens in the browser, not on the server. Zero server-side sleep, zero busy loop.

**Corrections Made:**
- Removed `time.sleep(2); st.rerun()` pattern entirely
- Added `st.components.v1.html()` with JS auto-reload matching sidebar `refresh_interval`
- Verified fix: HTTP 200 stable, no errors in stderr

---

### Prompt 7: Screenshot & Offline Map Export

**Prompt:**
> 截一张图吧，另外交互记录呢

**AI Response Summary:** Captured full-screen dashboard screenshot (3200×2000 → 1600×1000) via `PIL.ImageGrab` saved as both PNG and JPG in project folder. Created `export_map.py` standalone script that generates `rainfall_map.html` — a self-contained Folium map with colored markers and popups, openable without Streamlit. Updated `prompt_log.md` with Prompts 6-7.

**Files added:**
- `dashboard_screenshot.jpg` (404 KB) / `.png` (1.8 MB) — runtime screenshot
- `export_map.py` — standalone map generator
- `rainfall_map.html` (13 KB) — offline interactive Folium map

---

### Validation Notes (Updated)

| Check | Result |
|-------|--------|
| Classification (8.0/15.0/22.0 mm/h → green/yellow/red) | ✅ Correct |
| Folium markers colored by warning level | ✅ Verified |
| Popup displays city + rainfall + temp + humidity | ✅ Verified |
| Auto-refresh no longer crashes | ✅ Fixed (browser-side JS) |
| Simulation generates latitude-aware rainfall | ✅ North drier, south wetter |
| CSV history appends correctly | ✅ Verified |
| Standalone HTML map export | ✅ Working |

---

### Prompt 8: Manual Refresh Button (Replace Auto-Refresh)

**Prompt:**
> 早就过了5min了，在页面增加一个更新功能，点击更新即可更新

**AI Response Summary:** The JS `setTimeout` auto-reload proved unreliable in practice (timer didn't reliably fire). Replaced the entire auto-refresh mechanism with a manual approach: added a prominent blue `🔄 Refresh Data` button in the top-center of the page. Clicking it clears `st.session_state` cache and triggers `st.rerun()`, forcing a fresh data fetch for all 5 cities. After fetch, `next_refresh_at` is set to `inf` so widget interactions (checkbox toggles, etc.) use cached data instead of re-fetching. The sidebar was simplified: removed the refresh interval slider and redundant "Refresh Now" button, keeping only the alert log toggle and history checkbox. A `last_fetch_time` timestamp is displayed next to the refresh button.

**Corrections Made:**
- Removed `st.components.v1.html()` JS auto-reload entirely
- Removed sidebar `refresh_interval` slider (no longer applicable)
- Added `type="primary"` refresh button at page top with `st.columns` layout
- Set `st.session_state.next_refresh_at = float("inf")` after fetch to prevent re-fetch on widget interactions
- Stored `last_fetch_time` as readable timestamp string in session state
