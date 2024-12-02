import streamlit as st
import pandas as pd
import requests
import folium
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, FastMarkerCluster
from datetime import datetime

API_URL = "https://www.ndbc.noaa.gov/data/realtime2/<station_id>.txt"

st.set_page_config(page_title="FlowCast: NOAA Data", layout="wide", page_icon="🌊", initial_sidebar_state="expanded")

# Custom CSS for consistent banner, optimized layout, and active sidebar highlighting
st.markdown(
    """
    <style>
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
        .hero-subtitle, .styled-subheader {
            font-size: 1.5rem;
            font-weight: bold;
            color: #005f73;
            margin: 5px 0;
            font-family: "Consolas", monospace;
        }
        [data-testid="stSidebar"] {
            background-color: #0a9396;
            color: white;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

st.markdown('<div class="hero-title">Real-Time Data from NOAA</div>', unsafe_allow_html=True)


@st.cache_resource
def get_regions_hierarchy():
    """Cached definition of regions and stations."""
    return {
        "Atlantic (Tropical)": {
            "Cape Verde": {"id": "13001", "lat": 12.000, "lon": -23.000},
            "Martinique": {"id": "41040", "lat": 14.536, "lon": -53.136},
        },
        # Add other regions...
    }


@st.cache_data
def fetch_station_data(station_id):
    """Fetch station data and cache the result."""
    headers = {"Accept-Encoding": "gzip"}
    response = requests.get(API_URL.replace("<station_id>", station_id), headers=headers)
    if response.status_code == 200:
        data = response.text.splitlines()
        columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                   'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']
        df = pd.DataFrame([x.split() for x in data[2:] if x.strip() != ''], columns=columns)
        df = df.apply(pd.to_numeric, errors='coerce', axis=1)
        return df
    st.error("Failed to fetch data from NOAA API.")
    return None


def display_buoy_map(regions_hierarchy, selected_region="All Regions", selected_station=None, current_data=None):
    """Display a buoy map with selectable regions and stations."""
    center_lat, center_lon = 27.5, -60.0
    zoom_level = 2
    if selected_region != "All Regions":
        region_coords = [(station["lat"], station["lon"]) for station in regions_hierarchy[selected_region].values()]
        center_lat = sum(coord[0] for coord in region_coords) / len(region_coords)
        center_lon = sum(coord[1] for coord in region_coords) / len(region_coords)
        zoom_level = 3.5

    buoy_map = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level)
    marker_cluster = FastMarkerCluster([]).add_to(buoy_map)

    regions_to_display = (
        regions_hierarchy if selected_region == "All Regions" else {selected_region: regions_hierarchy[selected_region]}
    )
    for region, stations in regions_to_display.items():
        for station_name, station_data in stations.items():
            is_selected = selected_region != "All Regions" and selected_station == station_name
            icon_color = "green" if is_selected else "blue"
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


def render_API():
    """Render NOAA data with selectable region and station."""
    regions_hierarchy = get_regions_hierarchy()
    region_options = ["All Regions"] + list(regions_hierarchy.keys())
    selected_region = st.sidebar.selectbox("Select Region", region_options)
    selected_station = None
    if selected_region != "All Regions":
        selected_station = st.sidebar.selectbox("Select Station", list(regions_hierarchy[selected_region].keys()))

    if selected_station:
        station_id = regions_hierarchy[selected_region][selected_station]["id"]
        with st.spinner("Fetching data..."):
            df_api = fetch_station_data(station_id)
            if df_api is not None:
                current_data = {
                    "WTMP": df_api["WTMP"].iloc[-1] if "WTMP" in df_api.columns else "N/A",
                    "APD": df_api["APD"].iloc[-1] if "APD" in df_api.columns else "N/A",
                    "ATMP": df_api["ATMP"].iloc[-1] if "ATMP" in df_api.columns else "N/A",
                    "WSPD": df_api["WSPD"].iloc[-1] if "WSPD" in df_api.columns else "N/A",
                }
                st.markdown(f"**Last Updated:** {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S UTC')}")
                st.dataframe(df_api)
                st.line_chart(df_api[["WTMP", "APD", "ATMP", "WSPD"]])
                display_buoy_map(regions_hierarchy, selected_region, selected_station, current_data)
                st.download_button(
                    label="Download Data as CSV",
                    data=df_api.to_csv(index=False),
                    file_name=f"{selected_station}_data.csv",
                    mime="text/csv"
                )
    else:
        display_buoy_map(regions_hierarchy)


render_API()
