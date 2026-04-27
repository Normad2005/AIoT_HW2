import pandas as pd
import os
import folium

# Coordinates for Taiwan regions
REGION_COORDS = {
    "北部": (25.08, 121.56),
    "中部": (24.15, 120.67),
    "南部": (22.63, 120.30),
    "東北部": (24.76, 121.76),
    "東部": (23.98, 121.61),
    "東南部": (22.76, 121.14),
    # English fallbacks
    "Northern": (25.08, 121.56),
    "Central": (24.15, 120.67),
    "Southern": (22.63, 120.30),
    "Northeastern": (24.76, 121.76),
    "Eastern": (23.98, 121.61),
    "Southeastern": (22.76, 121.14)
}

def get_temp_color(temp):
    """Return color based on temperature rules."""
    if pd.isna(temp):
        return 'gray'
    if temp < 20:
        return 'blue'
    elif 20 <= temp <= 25:
        return 'green'
    elif 25 < temp <= 30:
        return 'yellow'
    else:
        return 'red'

def create_weather_map(df, selected_date=None):
    """
    Generate a Folium map with weather markers for a specific date.
    """
    # Center map on Taiwan
    m = folium.Map(location=[23.6978, 120.9605], zoom_start=7)
    
    if df.empty:
        return m
        
    # Filter data by date if provided
    if selected_date:
        map_df = df[df['date'] == selected_date]
    else:
        # Default to the earliest available date
        earliest_date = df['date'].min()
        map_df = df[df['date'] == earliest_date]

    for _, row in map_df.iterrows():
        region = row['region']
        
        # Find coordinates, skip if region not defined
        coords = REGION_COORDS.get(region)
        if not coords:
            # Fallback trying to match partial string
            for key, val in REGION_COORDS.items():
                if key in region:
                    coords = val
                    break
                    
        if not coords:
            continue
            
        avg_temp = row['avg_temp']
        color = get_temp_color(avg_temp)
        
        # Format HTML for popup
        popup_html = f"""
        <div style='width: 150px'>
            <b>{region}</b><br>
            日期: {row['date']}<br>
            最低溫: {row['min_temp']}°C<br>
            最高溫: {row['max_temp']}°C<br>
            平均溫: {row['avg_temp']:.1f}°C
        </div>
        """
        
        # Add CircleMarker
        folium.CircleMarker(
            location=coords,
            radius=15,
            popup=folium.Popup(popup_html, max_width=200),
            tooltip=f"{region} ({avg_temp}°C)",
            color='black',
            weight=1,
            fill=True,
            fill_color=color,
            fill_opacity=0.7
        ).add_to(m)
        
    return m

def load_data(filename="weather_data.csv"):
    """
    Load processed weather data from CSV.
    """
    if os.path.isfile(filename) and os.stat(filename).st_size > 0:
        return pd.read_csv(filename)
    return pd.DataFrame()
