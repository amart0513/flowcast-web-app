import streamlit as st
import pandas as pd
import plotly.express as px

# Page Configuration
st.set_page_config(page_title="FlowCast: Data Analysis", layout="wide", page_icon="🌊")

# Custom CSS for Styling
st.markdown(
    """
    <style>
        /* Banner Styling */
        .hero-title {
            font-size: 3rem;
            font-weight: bold;
            color: white;
            text-align: center;
            background: linear-gradient(135deg, #005f73, #0a9396);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 30px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0a9396; /* Lighter blue from the banner gradient */
            color: white;
        }

        /* Sidebar Titles */
        [data-testid="stSidebar"] h3 {
            color: white;
            font-weight: bold;
        }

        /* Metric Box Styling */
        .metric-box {
            background-color: rgba(255, 255, 255, 0.1); /* Semi-transparent white */
            border: 1px solid rgba(255, 255, 255, 0.3);
            border-radius: 8px;
            padding: 15px;
            margin-bottom: 15px;
            text-align: center;
            color: white; /* White text for contrast */
            font-weight: bold;
        }

        /* Subheader Styling */
        .styled-subheader {
            font-size: 1.5rem;
            font-weight: bold;
            color: #005f73;
            margin-bottom: 15px;
        }

        /* Map Container Styling */
        .map-container {
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.95); /* Transparent white */
            border: 2px solid #005f73;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Banner Title
st.markdown('<div class="hero-title">Data Analysis</div>', unsafe_allow_html=True)


def render_data():
    # Dataset Selection
    dataset_toggle = st.radio("Choose Dataset", ["Default Dataset", "Upload Your Own"], help="Select a dataset to analyze.")

    # File Upload
    if dataset_toggle == "Upload Your Own":
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully.")
        else:
            st.warning("Please upload a CSV file to proceed.")
            return
    else:
        df = pd.read_csv("oct25-2024.csv")
        st.info("Using the default dataset.")

    # Validate Data
    required_columns = ['Depth m', 'Temp °C', 'pH', 'ODO mg/L']
    for column in required_columns:
        if column not in df.columns:
            st.error(f"Missing column: {column}. Please upload a valid CSV file.")
            return

    if df.isnull().values.any():
        st.warning("Data contains NaN values. Please clean your data.")

    # Sidebar Metrics for Key Parameters
    st.sidebar.markdown("<h3>Key Water Quality Metrics</h3>", unsafe_allow_html=True)

    # Dissolved Oxygen Metric
    avg_odo = df['ODO mg/L'].mean()
    st.sidebar.markdown(
        f"<div class='metric-box'>Dissolved Oxygen (ODO)<br><span style='font-size: 1.2rem;'>{avg_odo:.2f} mg/L</span></div>",
        unsafe_allow_html=True,
    )

    # Temperature Metric
    avg_temp = df['Temp °C'].mean()
    st.sidebar.markdown(
        f"<div class='metric-box'>Temperature<br><span style='font-size: 1.2rem;'>{avg_temp:.2f} °C</span></div>",
        unsafe_allow_html=True,
    )

    # pH Metric
    avg_ph = df['pH'].mean()
    st.sidebar.markdown(
        f"<div class='metric-box'>pH Level<br><span style='font-size: 1.2rem;'>{avg_ph:.2f}</span></div>",
        unsafe_allow_html=True,
    )

    # Depth Metric
    avg_depth = df['Depth m'].mean()
    st.sidebar.markdown(
        f"<div class='metric-box'>Depth<br><span style='font-size: 1.2rem;'>{avg_depth:.2f} m</span></div>",
        unsafe_allow_html=True,
    )

    # Filtered Data
    filtered_df = df.copy()

    st.metric(label="Total Data Points", value=len(filtered_df))

    # Tabs for Visualizations
    Scatter_Plots_tab, Maps_tab, Line_Plots_tab, threeD_Plots_tab, Raw_Plots_tab = st.tabs(
        ["Scatter Plots", "Maps", "Line", "3D Plots", "Raw Data"]
    )

    # Scatter Plot Tab
    with Scatter_Plots_tab:
        st.markdown('<p class="styled-subheader">Scatter Plot</p>', unsafe_allow_html=True)
        fig = px.scatter(
            filtered_df,
            x="Depth m",
            y="Temp °C",
            size="pH",
            color="ODO mg/L",
            color_continuous_scale=px.colors.sequential.Turbo,
            template="plotly_white",
        )
        st.plotly_chart(fig)

    # Maps Tab
    with Maps_tab:
        st.markdown('<p class="styled-subheader">Maps</p>', unsafe_allow_html=True)
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            fig = px.scatter_mapbox(
                filtered_df,
                lat="Latitude",
                lon="Longitude",
                hover_data=["Depth m", "pH", "Temp °C", "ODO mg/L"],
                color="ODO mg/L",
                color_continuous_scale=px.colors.sequential.Turbo,
                zoom=12,
                mapbox_style="carto-positron",
            )
            st.plotly_chart(fig, use_container_width=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.error("Missing 'Latitude' or 'Longitude' columns in data.")

    # Line Plot Tab
    with Line_Plots_tab:
        st.markdown('<p class="styled-subheader">Line Plot</p>', unsafe_allow_html=True)
        color = st.color_picker("Choose a color", "#081E3F")
        fig = px.line(filtered_df, x=filtered_df.index, y="ODO mg/L", template="plotly_white")
        fig.update_traces(line_color=color)
        st.plotly_chart(fig)

    # 3D Plot Tab
    with threeD_Plots_tab:
        st.markdown('<p class="styled-subheader">3D Plot</p>', unsafe_allow_html=True)
        fig = px.scatter_3d(
            filtered_df,
            x="Longitude",
            y="Latitude",
            z="Depth m",
            color="ODO mg/L",
            color_continuous_scale=px.colors.sequential.Turbo,
            template="plotly_white",
        )
        fig.update_scenes(zaxis_autorange="reversed")
        st.plotly_chart(fig)

    # Raw Data Tab
    with Raw_Plots_tab:
        st.markdown('<p class="styled-subheader">Fetched Data</p>', unsafe_allow_html=True)
        st.dataframe(filtered_df)
        st.markdown('<p class="styled-subheader">Descriptive Statistics</p>', unsafe_allow_html=True)
        st.dataframe(filtered_df.describe())


# Render Data Analysis Page
render_data()
