import streamlit as st
import folium
from streamlit_folium import st_folium

# Sample Data for Zones
zone_data = [
    {
        "name": "Biscayne Bay",
        "basin_name": "Florida Southeast Coast",
        "water_type": "Estuary",
        "size": "189.25 sq. miles",
        "nutrients": """
            Nutrients like nitrogen and phosphorus are naturally present in water 
            and necessary for healthy growth of plants and animals. However, 
            excessive nutrients can lead to harmful algal blooms.
        """,
        "chlorophyll": "Chlorophyll-a is an indicator of algal concentration in water bodies."
    },
    # Add more zones here
]

# Create Base Map
base_map = folium.Map(location=[25.7617, -80.1918], zoom_start=7)

# Add Polygons or Markers with Popup Cards
for zone in zone_data:
    popup_html = f"""
    <div style="width:300px; font-family:sans-serif;">
        <h4>{zone['name']}</h4>
        <table style="width:100%; border:1px solid black; border-collapse: collapse;">
            <tr><th style="text-align:left;">Waterbody Name</th><td>{zone['name']}</td></tr>
            <tr><th style="text-align:left;">Basin Name</th><td>{zone['basin_name']}</td></tr>
            <tr><th style="text-align:left;">Water Type</th><td>{zone['water_type']}</td></tr>
            <tr><th style="text-align:left;">Size</th><td>{zone['size']}</td></tr>
        </table>
        <br>
        <b>Nutrients:</b> <p>{zone['nutrients']}</p>
        <b>Chlorophyll-a:</b> <p>{zone['chlorophyll']}</p>
    </div>
    """
    popup = folium.Popup(popup_html, max_width=400)
    folium.Marker(
        location=[27.9506, -82.4572],  # Replace with zone-specific coordinates
        popup=popup,
        tooltip=zone['name']
    ).add_to(base_map)

# Display the Map
st_folium(base_map, width=800, height=600)
