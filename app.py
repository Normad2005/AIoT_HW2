import streamlit as st
import pandas as pd
import sqlite3
from streamlit_folium import st_folium
import subprocess

from utils import create_weather_map, load_data

st.set_page_config(page_title="台灣氣象儀表板", layout="wide")

st.title("台灣氣象儀表板")

# Sidebar controls
st.sidebar.header("控制面版")
if st.sidebar.button("獲取最新資料 (執行 fetch_weather.py)"):
    with st.spinner("正在從氣象署 API 獲取資料..."):
        try:
            # Run the fetch_weather.py script to update CSV and SQLite
            result = subprocess.run(["python", "fetch_weather.py"], capture_output=True, text=True)
            if result.returncode == 0:
                st.sidebar.success("資料更新成功！")
            else:
                st.sidebar.error(f"資料更新出錯: {result.stderr}")
        except Exception as e:
            st.sidebar.error(f"執行出錯: {e}")

def load_data_from_db(db_name="data.db"):
    """HW2-4: 從 SQLite3 資料庫查詢資料"""
    try:
        conn = sqlite3.connect(db_name)
        query = "SELECT regionName, dataDate, mint as MinT, maxt as MaxT FROM TemperatureForecasts"
        df = pd.read_sql_query(query, conn)
        conn.close()
        return df
    except Exception as e:
        return pd.DataFrame()

# Custom CSS to make tabs larger
st.markdown("""
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 20px;
        font-weight: bold;
    }
</style>
""", unsafe_allow_html=True)

# Create tabs for different functionalities (Interactive Map first to make it default)
tab1, tab2 = st.tabs(["互動式氣溫地圖", "各地區氣溫趨勢"])

with tab2:
    st.header("各地區氣溫預報應用")
    
    # 1. 從 SQLite 載入資料
    df_db = load_data_from_db()
    
    if not df_db.empty:
        # 2. 提供下拉選單，讓使用者選擇地區
        regions = df_db['regionName'].unique()
        selected_region = st.selectbox("請選擇地區", regions)
        
        # 過濾該地區的資料
        region_df = df_db[df_db['regionName'] == selected_region].copy()
        
        # 準備畫圖用的資料 (以日期為 index)
        chart_data = region_df.set_index('dataDate')[['MinT', 'MaxT']]
        
        # 3. 使用折線圖顯示一週的氣溫資料
        st.subheader(f"{selected_region} 氣溫趨勢")
        st.line_chart(chart_data)
        
        # 4. 使用表格顯示一週的氣溫資料
        st.subheader("預報資料表格")
        display_region_df = region_df.drop(columns=['regionName']).reset_index(drop=True)
        st.dataframe(display_region_df, use_container_width=True, hide_index=True)
        
    else:
        st.warning("SQLite 資料庫為空或未找到。請點擊『獲取最新資料』。")

with tab1:
    st.header("台灣氣溫分佈圖")
    df_csv = load_data()
    
    if not df_csv.empty:
        # Let user select which date to visualize on the map
        available_dates = sorted(df_csv['date'].unique())
        selected_date = st.selectbox("請選擇地圖顯示日期:", available_dates)
        
        col1, col2 = st.columns([3, 2])
        
        with col1:
            st.subheader(f"氣溫地圖 ({selected_date})")
            # Generate and display map (use_container_width allows it to fit the column)
            weather_map = create_weather_map(df_csv, selected_date)
            st_folium(weather_map, height=600, use_container_width=True)
            
            # Legend
            st.markdown("""
            **平均溫度顏色說明:** 
            藍色: 低於 20°C | 綠色: 20-25°C | 黃色: 25-30°C | 紅色: 高於 30°C
            """)
            
        with col2:
            st.subheader("資料表格")
            display_df = df_csv[df_csv['date'] == selected_date].drop(columns=['date'])
            st.dataframe(display_df, use_container_width=True, height=600, hide_index=True)
    else:
        st.info("CSV 資料不可用。請先獲取資料。")
