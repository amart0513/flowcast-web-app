import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime
import random

# Set Page Configuration
st.set_page_config(page_title="FlowCast", layout="wide", page_icon="🌊", initial_sidebar_state="expanded")

# Apply Custom CSS
st.markdown(
    """
    <style>
        /* CSS Code from the layout provided */
        .hero-title {
            font-size: 2.8rem;
            font-weight: bold;
            color: white;
            text-align: center;
            background: linear-gradient(135deg, #005f73, #0a9396);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
            font-family: "Consolas", monospace;
            animation: fadeIn 1.5s ease-in-out;
        }
        .section-header {
            font-size: 2.5rem;
            text-align: center;
            margin-top: 40px;
            margin-bottom: 20px;
            color: #005f73;
            font-family: "Consolas", monospace;
        }
        .divider {
            border: 0;
            height: 1px;
            background: linear-gradient(to right, #005f73, #0a9396, #005f73);
            margin: 30px 0;
        }
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
        .back-to-top a {
            text-decoration: none;
            font-size: 1.2rem;
            color: #0a9396;
            font-weight: bold;
        }
        .back-to-top a:hover {
            color: #005f73;
            text-decoration: underline;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Hero Section
st.markdown('<h1 class="hero-title">Resource Page</h1>', unsafe_allow_html=True)

# Section Header
st.markdown('<h2 class="section-header">Harmful Conditions and Mitigation Strategies</h2>', unsafe_allow_html=True)

# Harmful Conditions Cards
st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("""
### Blue-Green Algae
- **Risks**: Produces harmful toxins affecting humans and aquatic life.
- **Prevention**: Reduce nutrient runoff from agriculture and avoid contact with algal blooms.
- **More Info**: [Report Algal Bloom](https://www.epa.gov/nutrientpollution/harmful-algal-blooms)
""")
st.markdown('</div>', unsafe_allow_html=True)

st.markdown('<div class="card">', unsafe_allow_html=True)
st.markdown("""
### Hypoxia (Low Oxygen Levels)
- **Risks**: Causes fish kills and long-term damage to ecosystems.
- **Prevention**: Implement aeration systems and limit industrial discharge.
- **More Info**: [Learn About Hypoxia](https://www.noaa.gov/education/resource-collections/ocean-coasts/ocean-dead-zones)
""")
st.markdown('</div>', unsafe_allow_html=True)

# Fish Kill Prediction System Section
st.markdown('<h2 class="section-header">Fish Kill Detection System</h2>', unsafe_allow_html=True)

# Live Update Functionality
st.markdown("**Last Update:** " + datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

# Simulated Data for Live Updates
locations = ["Zone 1", "Zone 2", "Zone 3", "Zone 4", "Zone 5"]
data = pd.DataFrame({
    "Location": locations,
    "Dissolved Oxygen (mg/L)": [round(random.uniform(3.5, 7.5), 1) for _ in locations],
    "Temperature (°C)": [round(random.uniform(20, 30), 1) for _ in locations],
    "Risk Level": [random.choice(["Low", "Medium", "High"]) for _ in locations]
})

# Filtering by Location
selected_location = st.sidebar.selectbox("Filter by Location", ["All"] + locations)

if selected_location != "All":
    filtered_data = data[data["Location"] == selected_location]
else:
    filtered_data = data

# Display Risk Table
st.dataframe(filtered_data)

# Visualization of Predictions
st.write("#### Dissolved Oxygen Levels Across Zones")
fig = px.bar(
    filtered_data,
    x="Location",
    y="Dissolved Oxygen (mg/L)",
    color="Risk Level",
    title="Dissolved Oxygen Levels and Risk Levels",
    labels={"Dissolved Oxygen (mg/L)": "Dissolved Oxygen (mg/L)", "Location": "Zone"}
)
st.plotly_chart(fig, use_container_width=True)

# Call to Action
st.markdown('<h2 class="section-header">Next Steps</h2>', unsafe_allow_html=True)
st.markdown("""
- **Monitor regularly**: Ensure dissolved oxygen, temperature, and other parameters are recorded frequently.
- **Engage with stakeholders**: Collaborate to reduce pollution sources and implement mitigation measures.
- **Refine predictions**: Use machine learning to improve fish kill detection accuracy.
""")