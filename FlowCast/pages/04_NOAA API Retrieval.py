import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

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
            margin-bottom: 20px;
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
    </style>
    """,
    unsafe_allow_html=True,
)

# Banner
st.markdown('<div class="hero-title">Real-Time Data from NOAA</div>', unsafe_allow_html=True)

# Function to display raw data
def raw_data(df):
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<div class="styled-subheader">Fetched Data</div>', unsafe_allow_html=True)
    st.dataframe(df)
    st.markdown('<div class="styled-subheader">Descriptive Statistics</div>', unsafe_allow_html=True)
    st.dataframe(df.describe())
    st.markdown('</div>', unsafe_allow_html=True)

# Function to render data from NOAA API
def render_API():
    # Sidebar for station selection
    stations = {
        '41122': 'Hollywood Beach, FL',
        '41114': 'Fort Pierce, FL',
        '41010': 'Cape Canaveral, FL',
        '41117': 'St. Augustine, FL',
        '41070': 'Daytona Beach, FL'
    }

    selected_station = st.sidebar.selectbox("Select a Station", list(stations.values()))
    station_id = [k for k, v in stations.items() if v == selected_station][0]

    response = requests.get(API_URL.replace('<station_id>', station_id))
    if response.status_code == 200:
        data = response.text.splitlines()
        columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                   'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']

        # Create the DataFrame
        df_api = pd.DataFrame([x.split() for x in data[2:] if x.strip() != ''], columns=columns)

        # Convert WTMP to numeric, forcing errors to NaN
        df_api['WTMP'] = pd.to_numeric(df_api['WTMP'], errors='coerce')

        # Station Title
        st.markdown(f'<h3 class="center-text styled-subheader">{selected_station}</h3>', unsafe_allow_html=True)

        # Info container with NOAA data explanation
        st.markdown(
            """
            <div class="card">
                <h4 style="color:#005f73; font-weight: bold;">Understanding NOAA Real-Time Data</h4>
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

        # Raw data display
        raw_data(df_api)

        # Filtered plot for water temperature
        valid_data = df_api['WTMP'].dropna()
        if not valid_data.empty:
            plt.figure(figsize=(10, 6))
            plt.plot(valid_data, marker='o', linestyle='-', color='b')
            plt.title(f"Water Temperature for {selected_station}", fontsize=16)
            plt.xlabel('Observation Time (Hours)', fontsize=14)
            plt.ylabel('Water Temperature (°C)', fontsize=14)
            st.pyplot(plt.gcf())
        else:
            st.warning(f"No valid data to display for {selected_station}.")
    else:
        st.error("Failed to fetch data. Please try again later.")

# Render the API function
render_API()
