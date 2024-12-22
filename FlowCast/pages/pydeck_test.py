import streamlit as st
import pydeck as pdk
import pandas as pd
import requests


def fetch_stations_in_area(b_box="-82.3,24.5,-80.0,26.6"):
    """
    Fetch water quality stations from the Water Quality Portal (WQP) using GeoJSON.
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
            "lat": coords[1],
            "lon": coords[0],
        })
    return pd.DataFrame(station_records)


def build_pydeck_map(df):
    """
    Creates a pydeck map layer with tooltips for station data.
    """
    # Define a layer
    layer = pdk.Layer(
        "ScatterplotLayer",
        data=df,
        get_position=["lon", "lat"],
        get_radius=200,  # Increase or decrease for marker size
        get_fill_color=[0, 0, 255],  # Blue markers
        pickable=True
    )

    # Define tooltips: show StationName, StationID
    tool_tip = {
        "html": "<b>Station Name:</b> {StationName} <br/>"
                "<b>Station ID:</b> {StationID}",
        "style": {
            "backgroundColor": "steelblue",
            "color": "white"
        }
    }

    # Create the Deck object
    view_state = pdk.ViewState(
        latitude=df["lat"].mean() if not df.empty else 0,
        longitude=df["lon"].mean() if not df.empty else 0,
        zoom=8,
        pitch=0
    )

    deck_map = pdk.Deck(
        initial_view_state=view_state,
        layers=[layer],
        tooltip=tool_tip
    )
    return deck_map


def main():
    st.set_page_config(page_title="Stations Map Demo", layout="wide")
    st.title("Water Quality Stations with PyDeck")
    st.write("Visualize station locations on an interactive map with tooltips.")

    # 1. Retrieve stations
    bbox = st.text_input("Bounding Box (minLon,minLat,maxLon,maxLat):",
                         value="-82.3,24.5,-80.0,26.6")

    if st.button("Fetch Stations"):
        stations_df = fetch_stations_in_area(bbox)
        if not stations_df.empty:
            st.success(f"Fetched {len(stations_df)} station(s).")
            st.dataframe(stations_df.head(10))

            # 2. Build PyDeck map
            st.subheader("Map (PyDeck)")
            deck_map = build_pydeck_map(stations_df)
            st.pydeck_chart(deck_map)
        else:
            st.warning("No stations found for the given bounding box.")


if __name__ == "__main__":
    main()
