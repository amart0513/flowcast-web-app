import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster
from datetime import date

API_URL = "https://www.ndbc.noaa.gov/data/realtime2/<station_id>.txt"

st.set_page_config(page_title="FlowCast: NOAA Data", layout="wide", page_icon="🌊", initial_sidebar_state="expanded")

# Custom CSS for consistent banner, optimized layout, and active sidebar highlighting
st.markdown(
    """
    <style>
        /* Consistent Banner */
        .hero-title {
            font-size: 3rem;
            font-weight: bold;
            color: white;
            text-align: center;
            background: linear-gradient(135deg, #005f73, #0a9396);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            font-family: "Consolas", monospace;
            animation: fadeIn 1.5s ease-in-out;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="hero-title">Real-Time Data from NOAA</div>', unsafe_allow_html=True)


# Function to display buoy map with enhancements
def display_buoy_map(regions_hierarchy, selected_region="Default", selected_station=None, current_data=None):
    # Set default map center
    center_lat, center_lon = 27.5, -60.0
    zoom_level = 4

    if selected_region != "Default":
        # Center map on the selected region
        region_coords = [(station["lat"], station["lon"]) for station in regions_hierarchy[selected_region].values()]
        center_lat = sum(coord[0] for coord in region_coords) / len(region_coords)
        center_lon = sum(coord[1] for coord in region_coords) / len(region_coords)
        zoom_level = 6  # Zoom closer to the region

    # Create a folium map
    buoy_map = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level)

    # Add MarkerCluster for better visualization
    marker_cluster = MarkerCluster().add_to(buoy_map)

    # Determine regions to display
    regions_to_display = (
        regions_hierarchy if selected_region == "Default" else {selected_region: regions_hierarchy[selected_region]}
    )

    # Add markers to the map
    for region, stations in regions_to_display.items():
        for station_name, station_data in stations.items():
            is_selected = selected_region != "Default" and selected_station == station_name
            icon_color = "red" if is_selected else "blue"
            popup_content = f"<b>{station_name}</b><br>Region: {region}"
            if is_selected and current_data:
                popup_content += f"""
                <ul>
                    <li><b>Water Temp:</b> {current_data.get('WTMP', 'N/A')}°C</li>
                    <li><b>Avg Wave Period:</b> {current_data.get('APD', 'N/A')} s</li>
                    <li><b>Atmos Pressure:</b> {current_data.get('ATMP', 'N/A')} hPa</li>
                    <li><b>Wind Speed:</b> {current_data.get('WSPD', 'N/A')} m/s</li>
                </ul>
                """

            folium.Marker(
                location=[station_data["lat"], station_data["lon"]],
                popup=folium.Popup(popup_content, max_width=250),
                tooltip=station_name,
                icon=folium.Icon(color=icon_color, icon="map-marker", prefix="fa")
            ).add_to(marker_cluster)

    return st_folium(buoy_map, width=800, height=600)


# Function to download data
def download_data(df):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as CSV",
        data=csv,
        file_name="noaa_data.csv",
        mime="text/csv",
    )


# Main render function
def render_API():
    # NOAA Regions and Stations
    regions_hierarchy = {
        "Atlantic (Tropical)": {
            "Cape Verde": {"id": "13001", "lat": 12.000, "lon": -23.000},
            "Martinique": {"id": "41040", "lat": 14.536, "lon": -53.136}
        },
        "Atlantic (West)": {
            "Bermuda": {"id": "41049", "lat": 27.505, "lon": -62.271},
            "St. Martin": {"id": "41004", "lat": 21.582, "lon": -58.630}
        },
        # Add more regions and buoys here...
    }

    # Add "Default" option for all buoys
    region_options = ["Default"] + list(regions_hierarchy.keys())
    selected_region = st.sidebar.selectbox("Select Region", region_options)

    if selected_region != "Default":
        station_options = list(regions_hierarchy[selected_region].keys())
        selected_station = st.sidebar.selectbox("Select Station", station_options)
    else:
        selected_station = None

    # Fetch data if a station is selected
    if selected_station:
        station_id = regions_hierarchy[selected_region][selected_station]["id"]

        with st.spinner("Fetching data..."):
            response = requests.get(API_URL.replace("<station_id>", station_id))
            if response.status_code == 200:
                data = response.text.splitlines()
                columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                           'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']

                # Create DataFrame
                df_api = pd.DataFrame([x.split() for x in data[2:] if x.strip() != ''], columns=columns)
                df_api = df_api.apply(pd.to_numeric, errors='coerce', axis=1)  # Convert all data to numeric

                # Extract the latest available data
                current_data = {
                    "WTMP": df_api["WTMP"].iloc[-1] if "WTMP" in df_api.columns else "N/A",
                    "APD": df_api["APD"].iloc[-1] if "APD" in df_api.columns else "N/A",
                    "ATMP": df_api["ATMP"].iloc[-1] if "ATMP" in df_api.columns else "N/A",
                    "WSPD": df_api["WSPD"].iloc[-1] if "WSPD" in df_api.columns else "N/A",
                }

                # Display map with the selected station highlighted
                display_buoy_map(regions_hierarchy, selected_region, selected_station, current_data)

                # Display raw data and descriptive statistics
                st.markdown("### Raw Data")
                st.dataframe(df_api)
                st.markdown("### Descriptive Statistics")
                st.dataframe(df_api.describe())

                # Download Button
                download_data(df_api)

                # Display interactive line charts
                st.markdown("### Interactive Charts")
                st.line_chart(df_api[["WTMP", "APD", "ATMP", "WSPD"]])

            else:
                st.error("Failed to fetch data from the NOAA API.")
    else:
        # Display map with all buoys
        display_buoy_map(regions_hierarchy)


# Run the app
render_API()
