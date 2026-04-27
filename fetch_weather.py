import requests
import pandas as pd
import urllib3

# Suppress insecure request warnings when verify=False is used
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def fetch_cwa_weather_data(api_key):
    """
    Fetch 7-day agricultural weather forecast data from Taiwan CWA API (F-A0010-001) using fileapi.
    """
    url = f"https://opendata.cwa.gov.tw/fileapi/v1/opendataapi/F-A0010-001?Authorization={api_key}&downloadType=WEB&format=JSON"
    
    try:
        # Handle SSL verification issues by using verify=False
        response = requests.get(url, verify=False)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def process_cwa_weather_data(data):
    """
    Parse the JSON response and extract date, region, min_temp, max_temp.
    Returns a pandas DataFrame with calculated avg_temp.
    """
    if not data or 'cwaopendata' not in data:
        return pd.DataFrame()

    extracted_data = []
    
    try:
        # Navigate the CWA JSON structure
        resources = data['cwaopendata'].get('resources', {})
        res = resources.get('resource', {})
        res_data = res.get('data', {})
        agr = res_data.get('agrWeatherForecasts', {})
        forecasts = agr.get('weatherForecasts', {})
        locations = forecasts.get('location', [])
        
        for loc in locations:
            region_name = loc.get('locationName')
            weather_elements = loc.get('weatherElements', {})
            
            # Dictionary to group elements by date
            date_records = {}
            
            # Process MinT
            min_t = weather_elements.get('MinT', {})
            for daily in min_t.get('daily', []):
                date = daily.get('dataDate')
                temp_str = daily.get('temperature')
                if date and temp_str is not None:
                    if date not in date_records:
                        date_records[date] = {'date': date, 'region': region_name}
                    try:
                        date_records[date]['min_temp'] = float(temp_str)
                    except ValueError:
                        date_records[date]['min_temp'] = None

            # Process MaxT
            max_t = weather_elements.get('MaxT', {})
            for daily in max_t.get('daily', []):
                date = daily.get('dataDate')
                temp_str = daily.get('temperature')
                if date and temp_str is not None:
                    if date not in date_records:
                        date_records[date] = {'date': date, 'region': region_name}
                    try:
                        date_records[date]['max_temp'] = float(temp_str)
                    except ValueError:
                        date_records[date]['max_temp'] = None
            
            # Add all records for this region to our main list
            extracted_data.extend(list(date_records.values()))
            
        df = pd.DataFrame(extracted_data)
        
        if not df.empty:
            # Calculate avg_temp = (min + max) / 2
            df['avg_temp'] = (df['min_temp'] + df['max_temp']) / 2
            
            # Ensure all required columns exist
            for col in ['date', 'region', 'min_temp', 'max_temp', 'avg_temp']:
                if col not in df.columns:
                    df[col] = None
                    
            # Reorder columns as requested
            df = df[['date', 'region', 'min_temp', 'max_temp', 'avg_temp']]
            
            # Sort by Region and Date
            df = df.sort_values(by=['region', 'date']).reset_index(drop=True)
            
        return df
        
    except Exception as e:
        print(f"Error parsing data: {e}")
        return pd.DataFrame()

import json

import sqlite3

def save_to_sqlite(df, db_name="data.db"):
    """
    HW2-3: Save temperature data to SQLite3 database and verify insertion.
    """
    try:
        conn = sqlite3.connect(db_name)
        cursor = conn.cursor()
        
        # 創建資料庫 Table，取名為 "TemperatureForecasts"
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS TemperatureForecasts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                regionName TEXT,
                dataDate TEXT,
                mint REAL,
                maxt REAL
            )
        ''')
        
        # 避免重複插入，先清空舊資料 (依作業需求可選)
        cursor.execute('DELETE FROM TemperatureForecasts')
        
        # 將氣溫資料存到資料庫
        for _, row in df.iterrows():
            cursor.execute('''
                INSERT INTO TemperatureForecasts (regionName, dataDate, mint, maxt)
                VALUES (?, ?, ?, ?)
            ''', (row['region'], row['date'], row['min_temp'], row['max_temp']))
            
        conn.commit()
        
        print("\n=== HW2-3: 檢查資料庫是否正確存入 ===")
        # 1. 列出所有地區名稱
        cursor.execute("SELECT DISTINCT regionName FROM TemperatureForecasts")
        regions = cursor.fetchall()
        print("1. 列出所有地區名稱:")
        for r in regions:
            print(f"  - {r[0]}")
            
        # 2. 列出中部地區的氣溫資料
        cursor.execute("SELECT * FROM TemperatureForecasts WHERE regionName = '中部地區'")
        central_data = cursor.fetchall()
        print("\n2. 列出中部地區的氣溫資料:")
        for row in central_data:
            print(f"  ID: {row[0]:<2} | Region: {row[1]:<5} | Date: {row[2]} | MinT: {row[3]} | MaxT: {row[4]}")
            
    except sqlite3.Error as e:
        print(f"SQLite Error: {e}")
    finally:
        if conn:
            conn.close()

if __name__ == "__main__":
    # Execution
    api_key = "CWA-52BD4636-E1D1-46B1-A1F9-446D0202C589"
    raw_data = fetch_cwa_weather_data(api_key)
    
    if raw_data:
        # HW2-1: 使用 json.dumps 觀察獲得的資料 (print a small snippet to avoid flooding the console)
        print("=== HW2-1: 觀察獲得的原始 JSON 資料 (部分) ===")
        print(json.dumps(raw_data, indent=4, ensure_ascii=False)[:1000] + "\n... (資料過長省略) ...\n")
        
        df = process_cwa_weather_data(raw_data)
        
        if not df.empty:
            # HW2-2: 使用 json.dumps 觀察提取的資料
            # Convert DataFrame back to a list of dicts to satisfy the json.dumps requirement
            extracted_list = df.to_dict(orient='records')
            print("=== HW2-2: 觀察提取的最高與最低氣溫資料 ===")
            print(json.dumps(extracted_list[:5], indent=4, ensure_ascii=False))
            print("... (僅顯示前 5 筆) ...\n")
            
            # Save results to "weather_data.csv", overwriting each run
            df.to_csv("weather_data.csv", index=False)
            print("Successfully processed and saved weather data to 'weather_data.csv'.")
            
            # HW2-3: 將氣溫資料儲存到 SQLite3 資料庫
            save_to_sqlite(df)
            
        else:
            print("Failed to parse the data into a DataFrame.")
    else:
        print("Failed to fetch data from CWA API.")
