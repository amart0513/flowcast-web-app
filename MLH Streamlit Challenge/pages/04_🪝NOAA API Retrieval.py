import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

IMAGE_FIU_BANNER = "media/FIU_Banner.png"
API_URL = "https://www.ndbc.noaa.gov/data/realtime2/<station_id>.txt"

st.set_page_config(page_title="FlowCast", layout="wide",
                   page_icon="🌊", initial_sidebar_state="expanded")


def raw_data(df):
    st.subheader("Fetched Data")
    st.dataframe(df)
    st.subheader("Descriptive Statistics")
    st.dataframe(df.describe())


def render_API():
    st.title("Real-Time Data from National Oceanic and Atmospheric Administration (NOAA)")

    # Define station IDs and their titles
    stations = {
        '41122': 'Hollywood Beach, FL',
        '41114': 'Fort Pierce, FL',
        '41010': 'Cape Canaveral, FL',
        '42036': 'Tampa, FL',
        '41070': 'Daytona Beach, FL'
    }

    def get_key(val):
        for key, value in stations.items():
            if value == val:
                return key
        return None

    # Sidebar for selecting a single station ID
    selected_station = st.sidebar.selectbox(
        "Select Station ID",
        list(stations.values()),
        index=0  # Default selection (first station)
    )

    station_id = get_key(selected_station)


    response = requests.get(API_URL.replace('<station_id>', station_id))
    if response.status_code == 200:
        data = response.text.splitlines()
        columns = ['YY', 'MM', 'DD', 'hh', 'mm', 'WDIR', 'WSPD', 'GST', 'WVHT', 'DPD', 'APD', 'MWD',
                   'PRES', 'ATMP', 'WTMP', 'DEWP', 'VIS', 'PTDY', 'TIDE']

        # Skip header rows if necessary and construct the DataFrame
        df_api = pd.DataFrame([x.split() for x in data[2:] if x.strip() != ''], columns=columns)

        # Convert WTMP to numeric, forcing errors to NaN
        df_api['WTMP'] = pd.to_numeric(df_api['WTMP'], errors='coerce')

        # Display the title for the current station
        st.divider()
        col1, col2, col3 = st.columns([1, 1, 1])
        with col2:
            st.title(stations[station_id])
        # Display the title for the current station

        # Display the raw data or any visualizations you want
        raw_data(df_api)

        # Check if we have valid data for water temperature
        valid_data = df_api['WTMP'].dropna()
        if not valid_data.empty:
            # Create a line chart using matplotlib
            plt.figure(figsize=(10, 5))
            plt.plot(valid_data.index, valid_data, marker='o', linestyle='-', color='b')
            plt.title(f'Water Temperature at {stations[station_id]}')
            plt.xlabel('Index')
            plt.ylabel('Water Temperature (°C)')
            plt.xticks(rotation=45)
            plt.grid()
            plt.legend(['Water Temperature'])

            # Display the matplotlib chart in Streamlit
            st.pyplot(plt)
        else:
            st.warning(f"No valid water temperature data available for the selected station.")
    else:
        st.error(f"Failed to retrieve data for station ID {station_id}. Please try again.")



render_API()