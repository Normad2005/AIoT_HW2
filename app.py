import streamlit as st
import pandas as pd
import sqlite3
from streamlit_folium import st_folium
import subprocess
import sys
import plotly.express as px

from utils import create_weather_map, load_data

st.set_page_config(page_title="台灣氣象儀表板", layout="centered")

st.title("台灣氣象儀表板")

@st.cache_data(ttl=3600, show_spinner=False)
def fetch_latest_data():
    """Automatically fetch latest weather data (caches for 1 hour)"""
    try:
        subprocess.run([sys.executable, "fetch_weather.py"], capture_output=True, text=True)
        return True
    except Exception:
        return False

# Trigger the auto-fetch (will only run once per hour)
with st.spinner("正在為您準備最新天氣資訊..."):
    fetch_latest_data()

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

# Custom CSS for Clean & Minimalist Light Theme
st.markdown("""
<style>
    /* Minimalist Light Theme */
    .stApp {
        background-color: #F0F2F5;
    }
    .stTabs [data-baseweb="tab-list"] {
        gap: 20px;
    }
    .stTabs [data-baseweb="tab"] {
        background-color: #ffffff;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        box-shadow: 0 -2px 5px rgba(0,0,0,0.02);
    }
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
        font-size: 18px;
        font-weight: 600;
        color: #2C3E50;
    }
    div[data-testid="stMetric"] {
        background-color: #ffffff;
        padding: 15px 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.04);
        border: 1px solid #E9ECEF;
    }
    div[data-testid="stMetric"] label {
        color: #6C757D !important;
        font-weight: 500;
    }
    h1, h2, h3 {
        color: #2C3E50;
        font-family: 'Inter', sans-serif;
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
        
        # 顯示近期摘要卡片
        st.subheader(f"{selected_region} 近期氣溫摘要")
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("最高溫 (一週)", f"{region_df['MaxT'].max()} °C")
        with col2:
            st.metric("最低溫 (一週)", f"{region_df['MinT'].min()} °C")
        with col3:
            avg_temp = round((region_df['MaxT'].mean() + region_df['MinT'].mean()) / 2, 1)
            st.metric("平均氣溫", f"{avg_temp} °C")

        st.markdown("<br>", unsafe_allow_html=True)
        
        # 3. 使用 Plotly 折線圖顯示一週的氣溫資料
        st.subheader("氣溫趨勢圖")
        fig = px.line(
            region_df, 
            x='dataDate', 
            y=['MinT', 'MaxT'], 
            markers=True,
            color_discrete_sequence=['#4F8BF9', '#FF6B6B']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_title="日期",
            yaxis_title="溫度 (°C)",
            legend_title="溫度類型",
            hovermode="x unified",
            margin=dict(l=0, r=0, t=30, b=0)
        )
        fig.update_xaxes(showgrid=True, gridwidth=1, gridcolor='#E9ECEF')
        fig.update_yaxes(showgrid=True, gridwidth=1, gridcolor='#E9ECEF')
        st.plotly_chart(fig, use_container_width=True)
        
        # 4. 使用表格顯示一週的氣溫資料
        st.subheader("預報資料表格")
        display_region_df = region_df.drop(columns=['regionName']).reset_index(drop=True)
        st.dataframe(display_region_df, use_container_width=True, hide_index=True)
        
    else:
        st.warning("暫無資料，請稍後再試或檢查 API 狀態。")

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
        st.info("暫無資料，請稍後再試或檢查 API 狀態。")
