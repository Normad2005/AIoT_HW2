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
* **2026-04-30 (UI/UX 升級與自動化)**
  * **Bug Fix**: 修復 Streamlit Cloud 佈署時 `ModuleNotFoundError: No module named 'requests'` 錯誤（將 `subprocess.run` 執行指令改為 `sys.executable` 以對應正確的虛擬環境）。
  * **UI 升級**: 導入極簡亮色系 (Clean & Minimalist Light) 主題，透過 `.streamlit/config.toml` 與自訂 CSS 增加卡片圓角、陰影與淺灰色背景 (`#F0F2F5`)。
  * **視覺優化**: 將原本的 `st.line_chart` 替換為 `plotly.express`，提供平滑曲線與更好的互動懸浮提示。
  * **自動化**: 移除手動「獲取資料」的側邊欄按鈕，改用 Streamlit 的 `@st.cache_data(ttl=3600)` 實作背景自動定期抓取，保持版面整潔。
  * **排版調整**: 將頁面佈局從 `wide` 改為 `centered`，使主內容區塊更集中，提升閱讀體驗與截圖便利性。