import pandas as pd
import numpy as np
from datetime import datetime, timedelta

np.random.seed(42)

# Generate earthquake-tsunami dataset for 2001-2022
start_date = datetime(2001, 1, 1)
end_date = datetime(2022, 12, 31)
date_range = (end_date - start_date).days

# Number of earthquakes to generate
n_earthquakes = 850

# Generate random dates
dates = [start_date + timedelta(days=int(x)) for x in np.sort(np.random.uniform(0, date_range, n_earthquakes))]

# Key earthquake regions (lat, lon) with higher activity
regions = {
    'Pacific Ring of Fire': [(35.0, 139.0), (9.0, 160.0), (-15.0, 167.0), (-30.0, 177.0), (2.0, 97.0)],
    'Mediterranean': [(35.0, 25.0), (37.0, 15.0), (39.0, 27.0)],
    'Mid-Atlantic Ridge': [(0.0, -25.0), (-20.0, -14.0)],
    'Indian Ocean': [(-10.0, 100.0), (-20.0, 115.0)],
}

data = []

for i, date in enumerate(dates):
    # Randomly select a region
    region_locs = []
    for region, locations in regions.items():
        region_locs.extend(locations)
    
    # Choose a base location and add some noise
    base_lat, base_lon = region_locs[i % len(region_locs)]
    latitude = base_lat + np.random.normal(0, 3)
    longitude = base_lon + np.random.normal(0, 3)
    
    # Constrain to valid ranges
    latitude = np.clip(latitude, -90, 90)
    longitude = np.clip(longitude, -180, 180)
    
    # Generate magnitude (Gutenberg-Richter law distribution)
    # Higher magnitudes are less frequent
    magnitude = np.random.exponential(1.5) + 4.0
    magnitude = np.minimum(magnitude, 9.5)
    magnitude = np.maximum(magnitude, 4.0)
    
    # Depth (typically 10-700 km)
    depth = np.random.exponential(50) + 10
    depth = np.minimum(depth, 700)
    depth = np.maximum(depth, 1)
    
    # Determine if tsunami occurred
    # Tsunamis are more likely with:
    # - Higher magnitudes (especially >7.0)
    # - Shallower depths (especially <70 km)
    # - Subduction zone locations
    
    is_subduction_zone = latitude < -20 or (latitude > 2 and latitude < 45 and longitude > 90 and longitude < 160)
    
    tsunami_probability = 0.05  # base rate
    
    if magnitude >= 7.0:
        tsunami_probability = 0.6
    elif magnitude >= 6.5:
        tsunami_probability = 0.4
    elif magnitude >= 6.0:
        tsunami_probability = 0.15
    
    if depth < 70:
        tsunami_probability *= 1.5  # Increase for shallow quakes
    else:
        tsunami_probability *= 0.5  # Decrease for deep quakes
    
    if is_subduction_zone:
        tsunami_probability *= 1.3
    
    tsunami_probability = min(tsunami_probability, 0.99)
    
    tsunami_occurred = np.random.random() < tsunami_probability
    
    # Additional parameters related to tsunamis
    if tsunami_occurred:
        tsunami_magnitude = np.random.uniform(1, 5)
        wave_height_m = np.random.exponential(3) + 1  # meters
        death_toll = int(np.random.exponential(50) * (tsunami_magnitude / 2))
        economic_impact_millions = int(np.random.exponential(500) + 10)
    else:
        tsunami_magnitude = 0
        wave_height_m = 0
        death_toll = int(np.random.exponential(5) if np.random.random() < 0.3 else 0)
        economic_impact_millions = int(np.random.exponential(100)) if np.random.random() < 0.2 else 0
    
    # Earthquake intensity estimate (Modified Mercalli)
    intensity = min(12, max(1, int(magnitude + 1 + np.random.normal(0, 0.5))))
    
    data.append({
        'Date': date,
        'Year': date.year,
        'Month': date.month,
        'Day': date.day,
        'Latitude': latitude,
        'Longitude': longitude,
        'Magnitude': round(magnitude, 2),
        'Depth_km': round(depth, 1),
        'Intensity': intensity,
        'Tsunami': 'Yes' if tsunami_occurred else 'No',
        'Tsunami_Magnitude': round(tsunami_magnitude, 2),
        'Wave_Height_m': round(wave_height_m, 2),
        'Death_Toll': death_toll,
        'Economic_Impact_Million_USD': economic_impact_millions
    })

df = pd.DataFrame(data)

# Sort by date
df = df.sort_values('Date').reset_index(drop=True)

# Save to CSV
df.to_csv('earthquakes_dataset.csv', index=False)

print(f"Dataset created with {len(df)} earthquake records")
print(f"Date range: {df['Date'].min()} to {df['Date'].max()}")
print(f"Tsunami events: {(df['Tsunami'] == 'Yes').sum()}")
print(f"\nFirst few records:")
print(df.head())
print(f"\nDataset shape: {df.shape}")
print(f"\nColumn names: {list(df.columns)}")
