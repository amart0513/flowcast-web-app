import streamlit as st
import pydeck as pdk
import pandas as pd

# Sample Data
data = pd.DataFrame({
    "zone": ["Zone 1", "Zone 2", "Zone 3"],
    "latitude": [27.9506, 28.5383, 26.1224],
    "longitude": [-82.4572, -81.3792, -80.1373],
    "quality": ["Good", "Moderate", "Poor"],
    "risk": ["Low", "Medium", "High"]
})

# Scatterplot Layer
scatterplot_layer = pdk.Layer(
    "ScatterplotLayer",
    data,
    get_position=["longitude", "latitude"],
    get_radius=10000,  # Adjust radius for better visibility
    get_fill_color=[0, 128, 255, 140],  # Blue with some transparency
    pickable=True  # Enables tooltip
)

# Tooltip Configuration
tooltip = {
    "html": """
        <b>Zone:</b> {zone}<br>
        <b>Water Quality:</b> {quality}<br>
        <b>Fish Kill Risk:</b> {risk}
    """,
    "style": {
        "backgroundColor": "steelblue",
        "color": "white",
        "fontSize": "14px",
        "padding": "10px"
    }
}

# Deck.gl Map
view_state = pdk.ViewState(
    latitude=27.994402,
    longitude=-81.760254,
    zoom=7,
    pitch=0
)

deck = pdk.Deck(
    layers=[scatterplot_layer],
    initial_view_state=view_state,
    tooltip=tooltip
)

# Streamlit Display
st.pydeck_chart(deck)
