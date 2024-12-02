import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import folium
from streamlit_folium import st_folium

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

# Banner
st.markdown('<div class="hero-title">Real-Time Data from NOAA</div>', unsafe_allow_html=True)


# Function to display raw data
def raw_data(df):
    st.markdown('<div class="styled-subheader">Fetched Data</div>', unsafe_allow_html=True)
    st.dataframe(df)
    st.markdown('<div class="styled-subheader">Descriptive Statistics</div>', unsafe_allow_html=True)
    st.dataframe(df.describe())
    st.markdown('</div>', unsafe_allow_html=True)


# Function to render data from NOAA API
def render_API():
    # NOAA Regions and Stations
    # only a small portion of selected data from the API -> want to expand this data globally
    regions_hierarchy = {
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

    # Display map
    st.markdown('<div class="styled-subheader">Buoy Locations</div>', unsafe_allow_html=True)
    buoy_map = folium.Map(location=[27.5, -60.0], zoom_start=4)  # Center map at an average location

    for region, stations in regions_hierarchy.items():
        for station_name, station_data in stations.items():
            folium.Marker(
                location=[station_data["lat"], station_data["lon"]],
                popup=f"{station_name} ({region})",
                tooltip=f"{station_name}",
            ).add_to(buoy_map)

    # Display the map in Streamlit
    st_folium(buoy_map, width=700, height=500)

    selected_region = st.sidebar.selectbox("Select Region", list(regions_hierarchy.keys()))
    if selected_region:
        selected_station = st.sidebar.selectbox("Select Station", list(regions_hierarchy[selected_region].keys()))
        if selected_region:
            station_id = regions_hierarchy[selected_region][selected_station]["id"]

            # Fetch NOAA Data
            response = requests.get(API_URL.replace("<station_id>", station_id))
            if response.status_code == 200:
                data = response.text.splitlines()
                columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                           'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']

            # Create DataFrame
            df_api = pd.DataFrame([x.split() for x in data[2:] if x.strip() != ''], columns=columns)
            df_api = df_api.apply(pd.to_numeric, errors='coerce', axis=1)  # Convert all data to numeric where possible

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

            # Station Title
            st.markdown(f'<div class="hero-subtitle">Region: {selected_region} <br> Station: {selected_station}</div>',
                        unsafe_allow_html=True)

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

            # Display the raw data dataframe
            st.dataframe(df_api)

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

            # Display the descriptive statistics of the dataframe
            st.dataframe(df_api.describe())

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

            st.markdown('<div class="styled-subheader">Plots</div>',
                        unsafe_allow_html=True)

            # Determine which data points are available and create a list of plots
            plots = []
            if 'WTMP' in df_api:
                plots.append({
                    "title": "Water Temperature",
                    "data": df_api['WTMP'],
                    "color": "blue",
                    "ylabel": "Temperature (°C)",
                    "label": "Water Temperature (°C)"
                })

            if 'ATMP' in df_api:
                plots.append({
                    "title": "Atmospheric Pressure",
                    "data": df_api['ATMP'],
                    "color": "green",
                    "ylabel": "Pressure (hPa)",
                    "label": "Atmospheric Pressure (hPa)"
                })

            if 'APD' in df_api:
                plots.append({
                    "title": "Average Wave Period",
                    "data": df_api['APD'],
                    "color": "purple",
                    "ylabel": "Period (s)",
                    "label": "Average Wave Period (s)"
                })

            if 'WSPD' in df_api:
                plots.append({
                    "title": "Wind Speed",
                    "data": df_api['WSPD'],
                    "color": "red",
                    "ylabel": "Speed (m/s)",
                    "label": "Wind Speed (m/s)"
                })

            # Check if there are any plots to display
            if plots:
                # Create a 2x2 grid dynamically based on the number of available plots
                num_plots = len(plots)
                num_rows = (num_plots + 1) // 2  # Calculate number of rows for a 2x2 layout
                fig, axs = plt.subplots(num_rows, 2, figsize=(15, 5 * num_rows), constrained_layout=True)

                # Flatten the axes array for easy iteration
                axs = axs.flatten()

                # Generate the plots
                for i, plot in enumerate(plots):
                    axs[i].plot(df_api.index, plot["data"], marker='o', color=plot["color"], label=plot["label"])
                    axs[i].set_title(plot["title"])
                    axs[i].set_xlabel("Observation Time")
                    axs[i].set_ylabel(plot["ylabel"])
                    axs[i].legend()
                    axs[i].tick_params(axis='x', rotation=45)
                    axs[i].grid(alpha=0.5)

                # Hide any unused subplots
                for j in range(len(plots), len(axs)):
                    fig.delaxes(axs[j])

                # Display the plots
                st.pyplot(fig)
            else:
                # If no data is available
                st.error("Failed to fetch data for the selected station.")


        else:
            st.error("Failed to fetch data for the selected region.")


# Render the API function
render_API()
