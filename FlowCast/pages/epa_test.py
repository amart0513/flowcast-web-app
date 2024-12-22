import streamlit as st
import pandas as pd
import requests
from datetime import date


# =========================================================
# 1. Fetch station data from WQP (using bounding box only)
# =========================================================
def fetch_stations_in_area(b_box="-82.3,24.5,-80.0,26.6"):
    """
    Fetches water quality station data from the Water Quality Portal
    within a specified bounding box (no statecode to avoid 406 errors).

    Parameters
    ----------
    b_box : str
        Bounding box in the format: "minLon,minLat,maxLon,maxLat".
        Example: "-82.3,24.5,-80.0,26.6" targets part of South Florida.

    Returns
    -------
    pandas.DataFrame
        DataFrame with station metadata (StationID, StationName, coords, etc.).
        If no stations or an error occurs, returns an empty DataFrame.
    """
    base_url = "https://www.waterqualitydata.us/data/Station/search"
    params = {
        "bBox": b_box,  # bounding box only
        "dataProfile": "station",  # 'station' or 'simplestation'
        "mimeType": "geojson"  # request GeoJSON format
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.HTTPError as e:
        st.error(f"Error fetching stations: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An unknown error occurred: {e}")
        return pd.DataFrame()

    features = data.get("features", [])
    station_records = []
    for feature in features:
        props = feature.get("properties", {})
        geom = feature.get("geometry", {})
        coords = geom.get("coordinates", [None, None])

        station_records.append({
            "OrganizationID": props.get("organizationidentifier"),
            "OrganizationName": props.get("organizationformalname"),
            "StationID": props.get("stationidentifier"),
            "StationName": props.get("stationname"),
            "Latitude": coords[1],
            "Longitude": coords[0],
            "CountyName": props.get("countyname"),
            "StateName": props.get("statename"),
            "HUC": props.get("hydrologicunitcode")  # Hydrologic Unit Code
        })

    return pd.DataFrame(station_records)


# =========================================================
# 2. Fetch water quality "results" data from WQP (by site)
# =========================================================
def fetch_water_quality_data(site_id, start_date, end_date):
    """
    Fetches water quality measurements (Result data) from WQP
    for a single site, within a date range.

    Parameters
    ----------
    site_id : str
        Site identifier, e.g., "USGS-02323500"
    start_date : str
        Lower bound date (YYYY-MM-DD), e.g., "2023-01-01"
    end_date : str
        Upper bound date (YYYY-MM-DD), e.g., "2023-01-31"

    Returns
    -------
    pandas.DataFrame
        DataFrame with measurement results (CharacteristicName, ResultValue, etc.).
        If no data or an error occurs, returns an empty DataFrame.
    """
    base_url = "https://www.waterqualitydata.us/data/Result/search"
    params = {
        "siteid": site_id,
        "startDateLo": start_date,
        "startDateHi": end_date,
        "mimeType": "json"
    }
    try:
        response = requests.get(base_url, params=params)
        response.raise_for_status()
        data = response.json()
    except requests.HTTPError as e:
        st.error(f"Error fetching water quality data: {e}")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An unknown error occurred: {e}")
        return pd.DataFrame()

    results = data.get("results", [])
    records = []
    for r in results:
        measure = r.get("ResultMeasure", {})
        records.append({
            "Organization": r.get("OrganizationIdentifier"),
            "StationID": r.get("MonitoringLocationIdentifier"),
            "CharacteristicName": r.get("CharacteristicName"),
            "ResultValue": r.get("ResultMeasureValue"),
            "ResultUnit": measure.get("MeasureUnitCode"),
            "SampleFraction": r.get("ResultSampleFractionText"),
            "ActivityType": r.get("ActivityTypeCode"),
            "SampleCollectionDate": r.get("ActivityStartDate"),
            "Latitude": r.get("LatitudeMeasure"),
            "Longitude": r.get("LongitudeMeasure"),
        })

    return pd.DataFrame(records)


# ==================================
# 3. Streamlit App: Full Integration
# ==================================
def run_wqp_app():
    st.set_page_config(page_title="EPA WQP Full Demo", layout="wide")
    st.title("EPA Water Quality Portal (WQP) - Full Demo App")
    st.write("""
    This app demonstrates:
    1. Fetching station metadata (sites) within a bounding box 
       **without** combining it with other spatial filters, preventing 406 errors.
    2. Selecting a station to retrieve water quality measurements.
    """)

    # ---------------------------
    # A) Fetch and Display Stations
    # ---------------------------
    with st.expander("Step 1: Fetch Stations in an Area"):
        st.write("""
        Enter a bounding box to fetch station data. Format: 
        `minLongitude, minLatitude, maxLongitude, maxLatitude`.

        Example: `-82.3,24.5,-80.0,26.6` roughly covers part of South Florida.
        """)
        b_box_input = st.text_input("Bounding Box", value="-82.3,24.5,-80.0,26.6")

        if st.button("Fetch Stations"):
            with st.spinner("Fetching stations from WQP..."):
                stations_df = fetch_stations_in_area(b_box_input)
            if not stations_df.empty:
                st.success(f"Found {len(stations_df)} station(s).")
                st.dataframe(stations_df.head(50))

                # Optional: Let user pick a station from the results
                station_list = stations_df["StationID"].dropna().unique().tolist()
                selected_station = st.selectbox(
                    "Select a Station ID to explore water quality data",
                    options=station_list
                )
                st.session_state["stations_df"] = stations_df
                st.session_state["selected_station"] = selected_station
            else:
                st.warning("No stations found for the given bounding box.")

    # ---------------------------
    # B) Fetch Water Quality Data
    # ---------------------------
    st.write("---")
    with st.expander("Step 2: Fetch Water Quality Measurements"):
        # If we already have a station selection from Step 1, pre-fill that.
        selected_station = st.session_state.get("selected_station", "")
        st.write("""
        Retrieve measurement data (Results) for a particular station 
        within a date range.
        """)

        station_input = st.text_input("Station ID (e.g., USGS-02323500)", value=selected_station)
        col1, col2 = st.columns(2)
        with col1:
            start_date = st.date_input("Start Date", value=date(2023, 1, 1))
        with col2:
            end_date = st.date_input("End Date", value=date(2023, 1, 31))

        if st.button("Fetch Water Quality Data"):
            with st.spinner("Fetching water quality results..."):
                wq_data = fetch_water_quality_data(
                    station_input,
                    start_date.strftime("%Y-%m-%d"),
                    end_date.strftime("%Y-%m-%d")
                )
            if not wq_data.empty:
                st.success(f"Fetched {len(wq_data)} measurement record(s).")
                st.dataframe(wq_data.head(50))

                # Simple numeric summary if 'ResultValue' is numeric
                if "ResultValue" in wq_data.columns:
                    # Convert to numeric where possible
                    wq_data["NumericValue"] = pd.to_numeric(wq_data["ResultValue"], errors="coerce")
                    numeric_only = wq_data.dropna(subset=["NumericValue"])
                    if not numeric_only.empty:
                        st.write("### Basic Statistics by Characteristic Name")
                        stats_df = numeric_only.groupby("CharacteristicName")["NumericValue"].describe()
                        st.dataframe(stats_df)
            else:
                st.warning("No water quality data found for this station and date range.")


if __name__ == "__main__":
    run_wqp_app()
