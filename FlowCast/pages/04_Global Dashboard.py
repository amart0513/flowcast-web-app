import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import folium
from folium import Map, Popup, Marker, Icon
from streamlit_folium import st_folium
from folium.plugins import MarkerCluster, FastMarkerCluster
from datetime import datetime

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
        
        .hero-subtitle {
            font-size: 1.5rem;
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

        /* Consistent Subtitle and Subheader Styles */
        .styled-subheader {
            font-size: 1.5rem;
            font-weight: bold;
            color: #005f73;
            margin: 5px 0;
            font-family: "Consolas", monospace;
        }

        /* Divider Style */
        .divider {
            border-top: 2px solid #005f73;
            margin: 10px 0;
        }

        /* Center Text */
        .center-text {
            text-align: center;
            margin: 0;
            font-family: "Consolas", monospace;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0a9396;
            color: white;
            padding: 20px;
            font-family: "Consolas", monospace;
        }

        [data-testid="stSidebar"] h3 {
            color: white;
            font-weight: bold;
            margin-bottom: 15px;
            font-family: "Consolas", monospace;
            
        }

        [data-testid="stSidebar"] label {
            font-size: 1rem;
            color: white;
            font-family: "Consolas", monospace;
        }

        [data-testid="stSidebar"] button {
            background-color: #005f73;
            color: white;
            font-size: 1rem;
            border-radius: 8px;
            padding: 10px 15px;
            margin: 10px 0;
            border: none;
            cursor: pointer;
            transition: transform 0.2s, background-color 0.3s;
            font-family: "Consolas", monospace;
        }

        [data-testid="stSidebar"] button:hover {
            background-color: #ffffff;
            color: #005f73;
            transform: scale(1.05);
        }

        [data-testid="stSidebar"] .stSelectbox {
            background-color: rgba(255, 255, 255, 0.1);
            color: white;
            border-radius: 8px;
            padding: 5px;
            margin: 10px 0;
            font-family: "Consolas", monospace;
        }

        /* Highlight Active Sidebar Item */
        .sidebar-item.active {
            background-color: #005f73;
            color: white;
            padding: 10px 15px;
            border-radius: 8px;
            font-weight: bold;
            margin-bottom: 10px;
            box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        }

        .sidebar-item {
            padding: 10px 15px;
            color: white;
            font-weight: bold;
            margin-bottom: 10px;
            cursor: pointer;
            transition: background-color 0.3s, transform 0.2s;
            font-family: "Consolas", monospace;
        }

        .sidebar-item:hover {
            background-color: #ffffff;
            color: #005f73;
            transform: scale(1.05);
        }

        /* Card Styling */
        .card {
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
            transition: transform 0.2s ease-in-out, box-shadow 0.2s ease-in-out;
            font-family: "Consolas", monospace;
        }

        .card:hover {
            transform: translateY(-5px);
            box-shadow: 0 8px 16px rgba(0, 0, 0, 0.2);
        }
        /* Animation */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Function to display all the buoys fetched from the station
def display_buoy_map(regions_hierarchy, selected_region="All Regions", selected_station=None, current_data=None):
    """
    Display a Folium map with buoys for a specific region or all regions.
    Ensures the map is properly centered and zoomed.
    """
    # Default map center and zoom
    center_lat, center_lon = 27.5, -60.0
    zoom_level = 2

    if selected_region != "All Regions":
        # Center the map on the selected region
        region_coords = [(station["lat"], station["lon"]) for station in regions_hierarchy[selected_region].values()]
        center_lat = sum(coord[0] for coord in region_coords) / len(region_coords)
        center_lon = sum(coord[1] for coord in region_coords) / len(region_coords)
        zoom_level = 5 # Moderate zoom level for the region

    if selected_station:
        # Center the map on the selected station
        station_data = regions_hierarchy[selected_region][selected_station]
        center_lat, center_lon = station_data["lat"], station_data["lon"]
        zoom_level = 8  # Close zoom for the specific station

    # Create a folium map centered on the calculated coordinates
    buoy_map = folium.Map(location=[center_lat, center_lon], zoom_start=zoom_level, control_scale=True)

    # Add a MarkerCluster for the buoys
    marker_cluster = MarkerCluster().add_to(buoy_map)

    # Determine which regions to display
    regions_to_display = (
        regions_hierarchy if selected_region == "All Regions" else {selected_region: regions_hierarchy[selected_region]}
    )

    # Add markers for all buoys in the selected region(s)
    for region, stations in regions_to_display.items():
        for station_name, station_data in stations.items():
            is_selected = selected_station == station_name
            icon_color = "red" if is_selected else "blue"

            # Construct the popup content
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

            # Add a marker for each buoy
            folium.Marker(
                location=[station_data["lat"], station_data["lon"]],
                popup=folium.Popup(popup_content, max_width=250),
                tooltip=station_name,
                icon=folium.Icon(color=icon_color, icon="map-marker", prefix="fa")
            ).add_to(marker_cluster)

    # Render the map within Streamlit
    return st_folium(buoy_map, width=800, height=600)



# Function to download the data for researching purposes
def download_data(df):
    csv = df.to_csv(index=False)
    st.download_button(
        label="Download Data as a CSV file.",
        data=csv,
        file_name="noaa_data.csv",
        mime="text/csv",
    )

def info_marker():
    # Info container with NOAA data explanation
    st.markdown(
        """
            <div class="card">
                <h4 style="color:#005f73; font-weight: bold;">What does NOAA's data mean and why is it important?</h4>
                <p style="color:#252323;">NOAA’s data provides key insights into meteorological and oceanographic conditions. Below is an explanation of the parameters used:</p>
                <ul style="color:#252323;">
                    <li><strong>Date and Time (YY, MM, DD, hh, mm):</strong> Indicate the date and time in UTC when the data was recorded.</li>
                    <li><strong>Wind Data:</strong>
                        <ul>
                            <li><strong>WDIR:</strong> Wind Direction (degrees) — where the wind originates, measured in degrees from north.</li>
                            <li><strong>WSPD:</strong> Wind Speed (m/s) — the average wind speed recorded during the observation.</li>
                            <li><strong>GST:</strong> Gust Speed (m/s) — the highest wind speed recorded during gusts.</li>
                        </ul>
                    </li>
                    <li><strong>Wave Data:</strong>
                        <ul>
                            <li><strong>WVHT:</strong> Significant Wave Height (meters) — average height of the highest third of waves.</li>
                            <li><strong>DPD:</strong> Dominant Wave Period (seconds) — the period between the most frequent waves.</li>
                            <li><strong>APD:</strong> Average Wave Period (seconds) — the average period between waves.</li>
                        </ul>
                    </li>
                    <li><strong>Atmospheric Data:</strong>
                        <ul>
                            <li><strong>PRES:</strong> Atmospheric Pressure (hPa) — crucial for weather forecasting.</li>
                            <li><strong>ATMP:</strong> Air Temperature (°C) — the temperature of the surrounding air.</li>
                            <li><strong>DEWP:</strong> Dew Point (°C) — indicates humidity levels.</li>
                            <li><strong>PTDY:</strong> Pressure Tendency (hPa) — measures how pressure changes over time.</li>
                        </ul>
                    </li>
                    <li><strong>Oceanic Data:</strong>
                        <ul>
                            <li><strong>WTMP:</strong> Water Temperature (°C) — temperature of the water at the observation site.</li>
                            <li><strong>VIS:</strong> Visibility (meters) — how far one can see in the given conditions.</li>
                            <li><strong>TIDE:</strong> Tide Height (meters) — the current tide height.</li>
                        </ul>
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True
    )


def stats_describe(df_api):
    st.markdown('<div class="styled-subheader">Descriptive Statistics</div>', unsafe_allow_html=True)

    # Explanation of descriptive statistics
    st.markdown("""
                        <div class="card">
                            <p style="color:#252323;">
                                The descriptive statistics provide a summary of key statistical measures for each data column. 
                                These metrics include the mean (average), standard deviation, minimum, maximum, and quartiles, 
                                which help users quickly assess the distribution and variability of the data. 
                                For example, this section can reveal the average wind speed, temperature range, or the general trends in oceanographic and atmospheric conditions at the station.
                                Descriptive statistics allow users to gain insights into the overall behavior of the data without needing to perform manual calculations.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)

    # Display raw descriptive statistics
    descriptive_stats = df_api.describe()
    st.subheader("Table")
    st.dataframe(descriptive_stats)

    # Generate dynamic insights based on descriptive statistics
    st.markdown('<div class="styled-subheader">Dynamic Insights</div>', unsafe_allow_html=True)
    insights = []

    # Water Temperature (WTMP)
    if 'WTMP' in df_api.columns:
        temp_mean = descriptive_stats.loc['mean', 'WTMP']
        temp_std = descriptive_stats.loc['std', 'WTMP']
        temp_range = descriptive_stats.loc['max', 'WTMP'] - descriptive_stats.loc['min', 'WTMP']
        temp_insight = f"Water temperature has an average of {temp_mean:.1f}°C with a standard deviation of {temp_std:.1f}, indicating {'high variability' if temp_std > 2 else 'stable conditions'}. The range is {temp_range:.1f}°C."
        insights.append(temp_insight)

    # Average Wave Period (APD)
    if 'APD' in df_api.columns:
        apd_mean = descriptive_stats.loc['mean', 'APD']
        apd_std = descriptive_stats.loc['std', 'APD']
        apd_insight = f"Wave periods average {apd_mean:.1f} seconds with a standard deviation of {apd_std:.1f}, reflecting {'significant fluctuations' if apd_std > 1.5 else 'consistent wave timing'}."
        insights.append(apd_insight)

    # Atmospheric Pressure (ATMP)
    if 'ATMP' in df_api.columns:
        atmp_mean = descriptive_stats.loc['mean', 'ATMP']
        atmp_std = descriptive_stats.loc['std', 'ATMP']
        atmp_range = descriptive_stats.loc['max', 'ATMP'] - descriptive_stats.loc['min', 'ATMP']
        atmp_insight = f"Atmospheric pressure averages {atmp_mean:.1f} hPa with a standard deviation of {atmp_std:.1f}, showing {'stable conditions' if atmp_std < 1 else 'significant variability'}. The range is {atmp_range:.1f} hPa."
        insights.append(atmp_insight)

    # Wind Speed (WSPD)
    if 'WSPD' in df_api.columns:
        wspd_mean = descriptive_stats.loc['mean', 'WSPD']
        wspd_std = descriptive_stats.loc['std', 'WSPD']
        wspd_insight = f"Wind speed has an average of {wspd_mean:.1f} m/s with a standard deviation of {wspd_std:.1f}, indicating {'steady winds' if wspd_std < 2 else 'variable wind speeds'}."
        insights.append(wspd_insight)

    # Display the generated insights in a single card
    if insights:
        insights_html = """
            <div class="card">
                <ul style="color:#252323;">
        """
        # Add each insight as a list item
        for insight in insights:
            insights_html += f"<li>{insight}</li>"

        # Close the unordered list and the card
        insights_html += """
                </ul>
            </div>
        """

        # Display the card in Streamlit
        st.markdown(insights_html, unsafe_allow_html=True)


def data_describe():
    # Display station info and raw data
    st.markdown('<div class="styled-subheader">Fetched Data</div>', unsafe_allow_html=True)
    # Explanation of fetched data
    st.markdown("""
                        <div class="card">
                            <p style="color:#252323;">
                                This raw data is retrieved from the NOAA station. It shows individual observations and measurements 
                                collected from the selected station, such as wind speed, wave height, temperature, and atmospheric pressure. 
                                The data is presented in tabular format, providing a detailed view of the recorded conditions at each observation time.
                                This raw data serves as the foundation for understanding the real-time conditions at the monitoring site and is useful for 
                                analysis or further exploration.
                            </p>
                        </div>
                    """, unsafe_allow_html=True)


def main_data_and_describe():
    # Main Title and Data Description
    st.markdown('<div class="styled-subheader">Environmental Observations Dashboard</div>',
                unsafe_allow_html=True)
    st.markdown("""
                               <div class="card">
                                   <p> This dashboard presents real-time environmental data from the selected station, including:
                                       <li><strong>Water Temperature</strong>: Tracks changes in sea surface temperature.</li>
                                       <li><strong>Atmospheric Pressure</strong>: Indicates weather conditions and possible storm systems.</li>
                                       <li><strong>Average Wave Period</strong>: Reflects the average time between successive waves, which can inform ocean conditions.</li>
                                       <li><strong>Wind Speed</strong>: Provides insight into wind conditions, impacting maritime and weather systems.</li>
                                   </p>
                                   <p>Use this information for monitoring environmental changes, supporting research, and enhancing decision-making.</p>
                               </div>
                               """, unsafe_allow_html=True)

# plots header
def plots_header():
    st.markdown('<div class="styled-subheader">Line Plots</div>',
                unsafe_allow_html=True)


@st.cache_resource
def get_regions_hierarchy():
    """Cached definition of regions and stations."""
    return {
        "Atlantic (Tropical)": {
            "Cape Verde": {"id": "13001", "lat": 12.000, "lon": -23.000},
            "Martinique": {"id": "41040", "lat": 14.536, "lon": -53.136}
        },
        "Atlantic (West)": {
            "Bermuda": {"id": "41049", "lat": 27.505, "lon": -62.271},
            "St. Martin": {"id": "41004", "lat": 21.582, "lon": -58.630}
        },
        "Gulf of Mexico (East)/Florida": {
            "Hollywood Beach, FL": {"id": "41122", "lat": 26.001, "lon": -80.096},
            "Daytona Beach, FL": {"id": "41070", "lat": 29.289, "lon": -80.803},
            "Cape Canaveral, FL": {"id": "41010", "lat": 28.878, "lon": -78.467},
            "St. Augustine, FL": {"id": "41117", "lat": 29.999, "lon": -81.079}
        },
        "USA-Southeast": {
            "Charleston, SC": {"id": "41004", "lat": 32.502, "lon": -79.099},
            "Cape Hatteras, NC": {"id": "41002", "lat": 32.300, "lon": -75.400},
            "Virginia Beach, VA": {"id": "44014", "lat": 36.611, "lon": -74.842},
            "Cape May, NJ": {"id": "44009", "lat": 38.457, "lon": -74.702}
        },
        "USA-Southwest": {
            "San Diego, CA": {"id": "46047", "lat": 32.500, "lon": -119.500},
            "Montague Island, AK": {"id": "46076", "lat": 59.600, "lon": -148.000},
            "Santa Monica Bay, CA": {"id": "46221", "lat": 33.800, "lon": -118.600},
            "Port Orford, OR": {"id": "46015", "lat": 42.800, "lon": -124.800}
        },
        "Caribbean Sea": {
            "Kingston, JM": {"id": "42058", "lat": 17.800, "lon": -76.800},
            "Cozumel, MX": {"id": "42056", "lat": 20.300, "lon": -86.800},
            "San Juan, PR": {"id": "41053", "lat": 18.500, "lon": -66.100},
            "St. John, VI": {"id": "41052", "lat": 18.300, "lon": -64.700}
        }
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

# Function for the legend and what each means
def legend_status():
    # Define a legend with default Streamlit line chart colors
    default_colors = {
        "WTMP": "#ffb5c0",  # light pink
        "APD": "#1f77b4",  # blue
        "ATMP": "#8ec3e6",  # light blue
        "WSPD": "#d62728"  # red
    }

    # Legend Information for the Line Chart
    legend_html = """
        <div class="card">
            <h4 style="color:#005f73; font-weight: bold;">Legend</h4>
            <ul style="color:#252323;">
                <li><span style="color:{WTMP};"><b>Water Temperature (WTMP):</b></span> Monitors the temperature of the sea surface (°C).</li>
                <li><span style="color:{APD};"><b>Average Wave Period (APD):</b></span> Average time between successive wave crests (seconds).</li>
                <li><span style="color:{ATMP};"><b>Atmospheric Pressure (ATMP):</b></span> Current atmospheric pressure at the station (hPa).</li>
                <li><span style="color:{WSPD};"><b>Wind Speed (WSPD):</b></span> Average wind speed measured at the station (m/s).</li>
            </ul>
        </div>
    """.format(**default_colors)

    st.markdown(legend_html, unsafe_allow_html=True)

# Function to render data from NOAA API
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

                st.markdown(f'<div class="hero-subtitle">Region: {selected_region} '
                            f'<br> Station: {selected_station}</div>', unsafe_allow_html=True)

                st.markdown('<div class="styled-subheader">Buoy Locations</div>',
                            unsafe_allow_html=True)
                display_buoy_map(regions_hierarchy, selected_region, selected_station, current_data)

                #Fetched data info
                data_describe()
                st.dataframe(df_api)

                # Descriptive stats
                stats_describe(df_api)

                # =========================================
                # Environmental Observations Dashboard
                # =========================================
                main_data_and_describe()

                # =========================================
                # Trends at this station in this region
                # =========================================

                # Analyze key trends dynamically
                wtmp_trend = 'rising' if df_api['WTMP'].diff().mean() > 0 else 'declining'
                apd_trend = 'consistent' if df_api['APD'].std() < 1 else 'fluctuating significantly'
                wspd_trend = 'stable' if df_api['WSPD'].std() < 2 else 'highly variable'
                atmp_trend = 'steady' if df_api['ATMP'].std() < 1 else 'changing significantly'

                # Display key trends observed
                trends_html = f"""
                <div class="card">
                    <div class="styled-subheader"">Key Trends Observed for This Station</div>
                    <ul>
                        <li><b>Water Temperature:</b> The trend is <strong>{wtmp_trend}</strong> based on recent observations.</li>
                        <li><b>Wave Periods:</b> They are <strong>{apd_trend}</strong> during the observed timeframe.</li>
                        <li><b>Wind Speeds:</b> The conditions are <strong>{wspd_trend}</strong> over the analyzed period.</li>
                        <li><b>Atmospheric Pressure:</b> The data indicates <strong>{atmp_trend}</strong> patterns.</li>
                    </ul>
                </div>
                """
                # output results into the card "container"
                st.markdown(trends_html, unsafe_allow_html=True)

                # =========================================
                # Line Plots
                # =========================================

                st.line_chart(df_api[["WTMP", "APD", "ATMP", "WSPD"]])
                legend_status()

                st.download_button(
                    label="Download Data as CSV",
                    data=df_api.to_csv(index=False),
                    file_name=f"{selected_station}_data.csv",
                    mime="text/csv"
                )

                st.markdown(f"**Last Updated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S ETC')}")
    else:
        # Banner
        st.markdown('<div class="hero-title">Real-Time Data from NOAA</div>', unsafe_allow_html=True)
        info_marker()
        st.markdown('<div class="styled-subheader">Buoy Locations</div>', unsafe_allow_html=True)
        st.info("Please select a region to view learn more.")
        display_buoy_map(regions_hierarchy)


# Render the API function
render_API()
