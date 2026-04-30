# AIoT HW2 - 台灣氣象儀表板 (Taiwan Weather Dashboard)

這是一個基於 Streamlit 開發的台灣即時氣象儀表板。專案會自動從中央氣象署抓取最新的氣溫與天氣資料，並以極簡且現代化的介面呈現給使用者。

## 🌟 功能特色
- **即時天氣獲取**：自動在背景從氣象局 API 抓取資料，並具有快取機制以提升效能。
- **互動式氣溫地圖**：結合 Folium 地圖，透過不同顏色直觀呈現台灣各縣市的氣溫分佈。
- **各地區氣溫趨勢**：使用 Plotly 繪製精美的互動式折線圖，查看一週內的最高/最低溫度趨勢。
- **極簡美學設計**：採用淺灰色背景與白底卡片的乾淨 UI，提供絕佳的使用者體驗。

## 🚀 Live Demo
點擊這裡查看線上展示：[**Live Demo 網址**](https://aiothw2-v6gezgj3ijtkwyceddvrsm.streamlit.app/)

## 📸 網頁截圖
![Taiwan Weather Dashboard Screenshot](./screenshot.png)

## 📝 Development Log

### [2026-04-30] - UI/UX 升級與自動化 (Today)
- **Bug Fix**: 修復 Streamlit Cloud 佈署時 `ModuleNotFoundError: No module named 'requests'` 錯誤（將 `subprocess.run` 執行指令由 `python` 改為 `sys.executable` 以對應正確的虛擬環境）。
- **UI 升級**: 導入極簡亮色系 (Clean & Minimalist Light) 主題，透過 `.streamlit/config.toml` 與自訂 CSS 增加卡片圓角、陰影與淺灰色背景 (`#F0F2F5`)。
- **視覺優化**: 將原本的 `st.line_chart` 替換為 `plotly.express` 互動圖表，提供平滑曲線與更好的數據懸浮提示。
- **自動化**: 移除手動獲取資料的按鈕，改用 `@st.cache_data(ttl=3600)` 實作背景自動定期抓取，並加入 `st.metric` 指標摘要。
- **排版調整**: 將頁面佈局改為 `centered`，使內容區塊更集中，提升閱讀體驗與截圖便利性。

### [2026-04-27] - 核心功能開發與資料庫整合
- **專案初始化**: 建立 `app.py`, `fetch_weather.py`, `utils.py` 等專案結構。
- **API 整合**: 串接中央氣象署 CWA API (F-A0010-001)，並處理 SSL 驗證與 JSON 解析。
- **資料處理**: 實作 `avg_temp` 計算邏輯，並將預報資料同步儲存至 CSV 與 SQLite3 資料庫 (`data.db`)，完成 HW2-3 需求。
- **視覺化實作**: 在 `utils.py` 中利用 `folium` 根據氣溫動態標註地圖顏色。
- **儀表板開發**: 實作 Streamlit 分頁功能 (Tabs)，整合地圖顯示、下拉式地區選擇器與 7 日氣溫趨勢圖表，完成 HW2-4 需求。