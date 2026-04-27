# Development Log

## [2026-04-27]
- Initialized weather dashboard project.
- Created project structure: `app.py`, `fetch_weather.py`, `utils.py`, `weather_data.csv`, `requirements.txt`.
- Set up virtual environment and `requirements.txt`.
- Updated `fetch_weather.py` to use Taiwan CWA API (Endpoint `F-A0010-001`) instead of OpenWeatherMap.
- Implemented SSL verification bypass (`verify=False`) for CWA API requests to handle certificate issues.
- Parsed JSON to extract Region, Min/Max Temperature, and Date into a pandas DataFrame.
- Extended `fetch_weather.py` to format DataFrame with columns: `date`, `region`, `min_temp`, `max_temp`, `avg_temp`.
- Implemented logic to calculate `avg_temp` = (min_temp + max_temp) / 2.
- Updated script to save the parsed DataFrame to `weather_data.csv`, overwriting it on each run.
- Created map visualization utility in `utils.py` using `folium`. Configured Taiwan region coordinates and dynamic colored circle markers based on `avg_temp`.
- Rewrote `app.py` Streamlit dashboard to use the new local CSV workflow, display the interactive Folium map, and add a sidebar button to trigger `fetch_weather.py`.
- Updated `fetch_weather.py` to add `save_to_sqlite` function, fulfilling HW2-3. It creates `data.db`, populates the `TemperatureForecasts` table, and verifies insertion with SELECT queries.
- Updated `app.py` to fulfill HW2-4: integrated SQLite data loading (`data.db`), added a dropdown region selector, and implemented a `st.line_chart` alongside a datatable to visualize 7-day temperature trends. Organized UI with tabs and custom CSS.
- Initialized Git repository, added a `.gitignore` to exclude temporary/generated files, and pushed the complete project to `https://github.com/Normad2005/AIoT_HW2`.
