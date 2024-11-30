import streamlit as st
import pandas as pd
import plotly.express as px
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from joblib import load
import seaborn as sns
import os
import numpy as np

# Page Configuration
st.set_page_config(page_title="FlowCast: Combined Analysis", layout="wide", page_icon="🌊")

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
st.markdown('<div class="hero-title">FlowCast: Data and Predictive Analysis</div>', unsafe_allow_html=True)

# Dropdown for Navigation
section = st.selectbox(
    "Choose Section", ["Data Analysis", "Predictive Analysis", "Comparative Analysis"], help="Navigate between Data, "
                                                                                             "Predictive, "
                                                                                             "and Comparative Analysis."
)

# Function for Data Analysis
def data_analysis():
    st.markdown('<p class="styled-subheader">Data Analysis</p>', unsafe_allow_html=True)

    # Dataset Selection
    dataset_toggle = st.radio("Choose Dataset", ["Default Dataset", "Upload Your Own"], help="Select a dataset to analyze.")
    if dataset_toggle == "Upload Your Own":
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file:
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

    # Sidebar Metrics
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

    # Tabs for Visualizations
    Scatter_Plots_tab, Maps_tab, Line_Plots_tab, threeD_Plots_tab, Raw_Plots_tab = st.tabs(
        ["Scatter Plots", "Maps", "Line", "3D Plots", "Raw Data"]
    )

    with Scatter_Plots_tab:
        st.markdown('<p class="styled-subheader">Scatter Plot</p>', unsafe_allow_html=True)
        fig = px.scatter(
            df, x="Depth m", y="Temp °C", size="pH", color="ODO mg/L", color_continuous_scale=px.colors.sequential.Turbo
        )
        st.plotly_chart(fig)

    with Maps_tab:
        st.markdown('<p class="styled-subheader">Maps</p>', unsafe_allow_html=True)
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            fig = px.scatter_mapbox(
                df, lat="Latitude", lon="Longitude", hover_data=["Depth m", "Temp °C", "ODO mg/L"],
                color="ODO mg/L", zoom=10, mapbox_style="carto-positron"
            )
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.error("Missing 'Latitude' or 'Longitude' columns in data.")

    with Line_Plots_tab:
        st.markdown('<p class="styled-subheader">Line Plot</p>', unsafe_allow_html=True)
        fig = px.line(df, x=df.index, y="ODO mg/L")
        st.plotly_chart(fig)

    with threeD_Plots_tab:
        st.markdown('<p class="styled-subheader">3D Plot</p>', unsafe_allow_html=True)
        fig = px.scatter_3d(
            df, x="Longitude", y="Latitude", z="Depth m", color="ODO mg/L", color_continuous_scale=px.colors.sequential.Turbo
        )
        st.plotly_chart(fig)

    with Raw_Plots_tab:
        st.markdown('<p class="styled-subheader">Raw Data</p>', unsafe_allow_html=True)
        st.dataframe(df)

# Function for Predictive Analysis
def predictive_analysis():
    st.markdown('<p class="styled-subheader">Predictive Analysis</p>', unsafe_allow_html=True)

    # Preloaded Dummy Data
    def generate_dummy_data():
        data = {
            'Latitude': np.random.uniform(25.0, 26.0, 100),
            'Longitude': np.random.uniform(-80.0, -79.0, 100),
            'Depth m': np.random.uniform(0, 50, 100),
            'Temp °C': np.random.uniform(15, 30, 100),
            'pH': np.random.uniform(6.5, 8.5, 100),
            'ODO mg/L': np.random.uniform(4, 12, 100),
        }
        return pd.DataFrame(data)

    # Function to Predict Water Quality
    def predict_water_quality(df):
        st.markdown('<p class="styled-subheader">Model Predictions</p>', unsafe_allow_html=True)

        # Select relevant features for prediction
        features = df[['Depth m', 'Temp °C', 'pH', 'ODO mg/L']]
        st.write("**Features used for prediction**: Depth (m), Temperature (°C), pH Levels, and ODO (mg/L)")
        st.dataframe(features.head())

        # Check if model exists
        model_file = 'data.pkl'
        if os.path.exists(model_file):
            model = load(model_file)

            # Make predictions
            predictions = model.predict(features)

            # Display predictions
            st.markdown('<p class="styled-subheader">Predicted Dissolved Oxygen (ODO mg/L)</p>', unsafe_allow_html=True)
            prediction_df = df.copy()
            prediction_df['Predicted ODO mg/L'] = predictions
            st.dataframe(prediction_df[['Depth m', 'Temp °C', 'pH', 'Predicted ODO mg/L']])

            # Actual vs Predicted Analysis
            if 'ODO mg/L' in df.columns:
                true_values = df['ODO mg/L']
                mse = mean_squared_error(true_values, predictions)
                st.write(f"**Mean Squared Error (MSE):** {mse}")

                # Scatter Plot
                st.markdown('<p class="styled-subheader">Actual vs Predicted Dissolved Oxygen (ODO mg/L)</p>', unsafe_allow_html=True)
                plt.figure(figsize=(10, 6))
                plt.scatter(true_values, predictions, alpha=0.6)
                plt.plot([true_values.min(), true_values.max()], [true_values.min(), true_values.max()], 'r--', lw=2)
                plt.xlabel("Actual ODO mg/L")
                plt.ylabel("Predicted ODO mg/L")
                plt.title("Scatter Plot of Actual vs Predicted ODO")
                st.pyplot(plt)
                plt.clf()

                # Error Distribution
                st.markdown('<p class="styled-subheader">Error Distribution</p>', unsafe_allow_html=True)
                errors = true_values - predictions
                plt.figure(figsize=(10, 6))
                sns.histplot(errors, bins=30, kde=True)
                plt.xlabel("Prediction Error (Actual - Predicted ODO mg/L)")
                plt.title("Error Distribution of Predictions")
                st.pyplot(plt)
                plt.clf()

                # Line Plot
                st.markdown('<p class="styled-subheader">Line Plot of Actual and Predicted ODO over Index</p>', unsafe_allow_html=True)
                plt.figure(figsize=(10, 6))
                plt.plot(prediction_df.index, true_values, label='Actual ODO mg/L', color='blue')
                plt.plot(prediction_df.index, predictions, label='Predicted ODO mg/L', color='orange', linestyle='--')
                plt.xlabel("Index")
                plt.ylabel("ODO mg/L")
                plt.title("Line Plot of Actual vs Predicted ODO")
                plt.legend()
                st.pyplot(plt)
        else:
            st.error(f"Model file {model_file} not found. Train the model first.")

    # Function to Assess Fish Kill Risk
    def predict_fish_kill(df):
        st.markdown('<p class="styled-subheader">Fish Kill Risk Assessment</p>', unsafe_allow_html=True)

        # Select relevant features for prediction
        features = df[['Depth m', 'Temp °C', 'pH', 'ODO mg/L']]
        st.write("**Features used for prediction**: Depth (m), Temperature (°C), pH Levels, and Dissolved Oxygen (ODO mg/L)")
        st.dataframe(features.head())

        # Check if model exists
        model_file = 'data.pkl'
        if os.path.exists(model_file):
            model = load(model_file)

            # Make predictions
            predictions = model.predict(features)
            df['Predicted ODO mg/L'] = predictions

            # Assess Fish Kill Risk
            df['Risk Level'] = df['Predicted ODO mg/L'].apply(
                lambda odo: 'High' if odo < 4 else 'Moderate' if odo < 6 else 'Low'
            )

            # Display Risk Summary
            st.write("**Risk Level Summary**")
            st.dataframe(df['Risk Level'].value_counts())

            # Map Visualization
            st.markdown('<p class="styled-subheader">Risk Level Map</p>', unsafe_allow_html=True)
            fig = px.scatter_mapbox(
                df,
                lat="Latitude",
                lon="Longitude",
                color="Risk Level",
                color_discrete_map={
                    "Low": "green",
                    "Moderate": "yellow",
                    "High": "red",
                },
                hover_data=["Depth m", "Temp °C", "pH", "Predicted ODO mg/L"],
                zoom=8,
                mapbox_style="carto-positron",
            )
            st.plotly_chart(fig, use_container_width=True)

            # Display Risk Messages
            if 'High' in df['Risk Level'].values:
                st.warning("⚠️ Areas with High Risk of Fish Kill detected. Immediate action recommended.")
            elif 'Moderate' in df['Risk Level'].values:
                st.info("⚠️ Areas with Moderate Risk of Fish Kill detected. Monitoring required.")
            else:
                st.success("✅ All areas show Low Risk of Fish Kill.")
        else:
            st.error(f"Model file {model_file} not found. Train the model first.")

    # Toggle between Predictive Options
    option = st.selectbox("Choose Analysis Type", ["Water Quality Prediction", "Fish Kill Risk Assessment"])

    # Main Section for Predictive Analysis
    data_toggle = st.radio("Select Data Source", ["Upload CSV File", "Use Preloaded Dummy Data"], help="Choose how to provide data for predictions.")

    if data_toggle == "Upload CSV File":
        uploaded_file = st.file_uploader("Upload a CSV file for prediction", type=["csv"])
        if uploaded_file is not None:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully.")
            if option == "Water Quality Prediction":
                predict_water_quality(df)
            elif option == "Fish Kill Risk Assessment":
                predict_fish_kill(df)
        else:
            st.warning("Please upload a CSV file to get predictions.")
    else:
        st.write("Using preloaded dummy data for predictions.")
        dummy_df = generate_dummy_data()
        st.dataframe(dummy_df.head())
        if option == "Water Quality Prediction":
            predict_water_quality(dummy_df)
        elif option == "Fish Kill Risk Assessment":
            predict_fish_kill(dummy_df)


# Display the selected section
if section == "Data Analysis":
    data_analysis()
elif section == "Predictive Analysis":
    predictive_analysis()
