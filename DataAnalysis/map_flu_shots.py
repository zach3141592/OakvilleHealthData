import pandas as pd
import folium
from folium.plugins import HeatMap, MarkerCluster
from geopy.geocoders import Nominatim
import time
import random
from shapely.geometry import Point, Polygon

# Read the data
df = pd.read_csv('flu_data_new.csv')

# Initialize geocoder
geolocator = Nominatim(user_agent="flu_shot_map")

# Dictionary to store coordinates for each pharmacy
pharmacy_coords = {
    "Shoppers Drug Mart, 123 Lakeshore Rd W, Oakville": (43.4474, -79.6665),
    "Rexall, 245 Trafalgar Rd, Oakville": (43.4500, -79.7000),
    "Pharmasave, 156 Kerr St, Oakville": (43.4480, -79.6800),
    "Guardian Pharmacy, 89 Cornwall Rd, Oakville": (43.4490, -79.6900),
    "Walmart Pharmacy, 240 Leighland Ave, Oakville": (43.4510, -79.7100),
    "Costco Pharmacy, 1200 South Service Rd, Oakville": (43.4520, -79.7200),
    "Loblaw Pharmacy, 301 Cornwall Rd, Oakville": (43.4485, -79.6850),
    "Sobeys Pharmacy, 240 Leighland Ave, Oakville": (43.4510, -79.7100),
    "Medicine Shoppe, 345 Kerr St, Oakville": (43.4482, -79.6820),
    "IDA Pharmacy, 178 Lakeshore Rd E, Oakville": (43.4476, -79.6680)
}

# Define Oakville land boundary (area between Lakeshore Road East, Winston Churchill, Dundas, and Bronte)
oakville_boundary = Polygon([
    (-79.7935, 43.3863),  # Lakeshore Road and Winston Churchill intersection
    (-79.7935, 43.4727),  # Dundas Street and Winston Churchill intersection
    (-79.7127, 43.4727),  # Dundas Street and Bronte Road intersection
    (-79.7127, 43.3927),  # Lakeshore Road and Bronte Road intersection
    (-79.7935, 43.3863)   # Back to start (Lakeshore and Winston Churchill)
])

def generate_random_oakville_coords():
    while True:
        # Generate random point within the new boundary
        lon = random.uniform(-79.7935, -79.7127)  # Between Winston Churchill and Bronte
        lat = random.uniform(43.3863, 43.4727)    # Between Lakeshore and Dundas
        point = Point(lon, lat)
        
        # Check if point is within Oakville boundary
        if oakville_boundary.contains(point):
            return (lat, lon)

# Create the map centered on the new area
oakville_center = [43.4295, -79.7531]  # Center of the new boundary area
m = folium.Map(
    location=oakville_center,
    zoom_start=12,  # Adjusted zoom level
    tiles='OpenStreetMap',  # Using OpenStreetMap for better alignment
    control_scale=True,  # Adding scale control
    max_zoom=19  # Increased max zoom level
)

# Create a MarkerCluster for pharmacies
pharmacy_cluster = MarkerCluster(name="Pharmacies").add_to(m)

# Add pharmacy markers with counts
pharmacy_counts = df['Pharmacy Address'].value_counts()
max_count = pharmacy_counts.max()  # Get the maximum count for scaling

for address, coords in pharmacy_coords.items():
    count = pharmacy_counts[address]
    # Calculate radius based on count, with larger base size and better scaling
    radius = 15 + (count / max_count * 25)  # Base size of 15, scaled up to 40
    folium.CircleMarker(
        location=coords,
        radius=radius,  # Dynamic radius based on count
        popup=f"{address}<br>Flu Shots: {count}",
        color='blue',
        fill=True,
        fill_color='blue',
        fill_opacity=0.7,
        max_zoom=19  # Ensure visibility at all zoom levels
    ).add_to(m)  # Add directly to map instead of cluster

# Add Oakville boundary to the map
boundary_coords = [
    [43.3863, -79.7935],  # Lakeshore and Winston Churchill
    [43.4727, -79.7935],  # Dundas and Winston Churchill
    [43.4727, -79.7127],  # Dundas and Bronte
    [43.3927, -79.7127],  # Lakeshore and Bronte
    [43.3863, -79.7935]   # Back to start (Lakeshore and Winston Churchill)
]

folium.Polygon(
    locations=boundary_coords,
    color='red',
    fill=False,
    weight=3,  # Increased weight for better visibility
    opacity=0.8,
    name='Oakville Boundary'
).add_to(m)

# Add layer control
folium.LayerControl().add_to(m)

# Add title
title_html = '''
<div style="position: fixed; 
            top: 10px; 
            left: 50%;
            transform: translateX(-50%);
            z-index: 9999;
            background-color: white;
            padding: 10px;
            border: 2px solid grey;
            border-radius: 5px;
            font-size: 16px;
            font-weight: bold;">
    Oakville Flu Shot Distribution (Lakeshore to Dundas, Bronte to Winston Churchill)
</div>
'''
m.get_root().html.add_child(folium.Element(title_html))

# Save the map
m.save('oakville_flu_heatmap.html')

print("Map has been generated and saved as 'oakville_flu_heatmap.html'")
print("\nFlu Shot Distribution by Pharmacy:")
print(pharmacy_counts) 