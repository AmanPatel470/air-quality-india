import requests
import pandas as pd
from datetime import datetime, timedelta
import os

cities = {
    "Delhi": {"lat": 28.6139, "lon": 77.2090},
    "Mumbai": {"lat": 19.0760, "lon": 72.8777},
    "Bengaluru": {"lat": 12.9716, "lon": 77.5946},
    "Chennai": {"lat": 13.0827, "lon": 80.2707},
    "Kolkata": {"lat": 22.5726, "lon": 88.3639}
}

end_date = datetime.today().strftime('%Y-%m-%d')
start_date = (datetime.today() - timedelta(days=365)).strftime('%Y-%m-%d')

all_data = []

print(f"Fetching data from {start_date} to {end_date}...")

for city, coords in cities.items():
    print(f"Downloading {city}...")
    
    # FIXED: Using dynamic coordinates and all pollutants
    url = f"https://air-quality-api.open-meteo.com/v1/air-quality?latitude={coords['lat']}&longitude={coords['lon']}&hourly=pm10,pm2_5,carbon_monoxide,nitrogen_dioxide,ozone&start_date={start_date}&end_date={end_date}"
    
    response = requests.get(url)
    data = response.json()
    
    if 'hourly' in data:
        df_city = pd.DataFrame(data['hourly'])
        df_city['City'] = city
        
        # FIXED: Removed the deprecated inplace=True
        df_city = df_city.rename(columns={
            'time': 'Date', 
            'pm2_5': 'PM2.5', 
            'pm10': 'PM10', 
            'carbon_monoxide': 'CO', 
            'nitrogen_dioxide': 'NO2', 
            'ozone': 'O3'
        })
        
        df_city['Date'] = pd.to_datetime(df_city['Date'])
        df_city['Date'] = df_city['Date'].dt.date 
        
        daily_df = df_city.groupby(['City', 'Date']).mean().reset_index()
        all_data.append(daily_df)

if all_data:
    final_df = pd.concat(all_data, ignore_index=True)
    
    def get_aqi_bucket(pm25):
        if pd.isna(pm25): return "Unknown"
        if pm25 <= 30: return "Good"
        elif pm25 <= 60: return "Satisfactory"
        elif pm25 <= 90: return "Moderate"
        elif pm25 <= 120: return "Poor"
        elif pm25 <= 250: return "Very Poor"
        else: return "Severe"
        
    final_df['AQI_Bucket'] = final_df['PM2.5'].apply(get_aqi_bucket)
    
    # FIXED: Using absolute path to the root directory
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    output_path = os.path.join(base_dir, 'data', 'clean', 'live_air_quality.csv')
    
    final_df.to_csv(output_path, index=False)
    print(f"\nSuccess! Saved {len(final_df)} rows to {output_path}")
else:
    print("Failed to fetch data. Check API response.")