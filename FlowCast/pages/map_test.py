import streamlit as st
import pandas as pd
import requests


def fetch_stations_in_area(b_box="-82.3,24.5,-80.0,26.6"):
    """
    Fetches water quality stations (sites) from the Water Quality Portal (WQP)
    using a bounding box query, requesting GeoJSON format.
    """
    base_url = "https://www.waterqualitydata.us/data/Station/search"
    params = {
        "bBox": b_box,
        "dataProfile": "station",
        "mimeType": "geojson"
    }
    response = requests.get(base_url, params=params)
    response.raise_for_status()
    data = response.json()

    features = data.get("features", [])
    station_records = []
    for feature in features:
        props = feature.get("properties", {})
        geom = feature.get("geometry", {})
        coords = geom.get("coordinates", [None, None])

        station_records.append({
            "StationID": props.get("stationidentifier"),
            "StationName": props.get("stationname"),
            "Latitude": coords[1],
            "Longitude": coords[0],
        })
    return pd.DataFrame(station_records)


def main():
    st.title("Water Quality Stations with Maps")
    st.write("Use this demo to visualize station locations on a map.")

    # 1. Fetch stations
    st.subheader("Station Retrieval")
    bbox = st.text_input("Bounding Box (minLon,minLat,maxLon,maxLat):",
                         value="-82.3,24.5,-80.0,26.6")

    if st.button("Fetch Stations"):
        stations_df = fetch_stations_in_area(b_box=bbox)
        if not stations_df.empty:
            st.write(f"Fetched {len(stations_df)} station(s).")
            st.dataframe(stations_df.head(10))

            # 2. Simple Map Visualization with st.map
            st.subheader("Map (st.map)")
            # st.map expects a DataFrame with columns: ["lat", "lon"]
            # We'll rename them if necessary:
            map_df = stations_df.rename(columns={"Latitude": "lat", "Longitude": "lon"})
            st.map(map_df[["lat", "lon"]])  # This shows a basic map with markers
        else:
            st.warning("No stations found for the given bounding box.")


if __name__ == "__main__":
    main()
