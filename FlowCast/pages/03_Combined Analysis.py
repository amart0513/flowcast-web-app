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
st.markdown('<div class="hero-title">FlowCast: Combined Analysis</div>', unsafe_allow_html=True)

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
        f"<div class='metric-box'>Temperature °C<br><span style='font-size: 1.2rem;'>{avg_temp:.2f} °C</span></div>",
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
            df, x="Depth m", y="Temp °C", size="pH", color="ODO mg/L", color_continuous_scale=px.colors.sequential.ice
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
            df, x="Longitude", y="Latitude", z="Depth m", color="ODO mg/L", color_continuous_scale=px.colors.sequential.ice
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


# Function for Comparative Analysis
def comparative_analysis():
    st.markdown('<p class="styled-subheader">Comparative Analysis: March 2024 - October 2024</p>', unsafe_allow_html=True)

    st.markdown(
        """
        <style>
        .info-container {
            background-color: #f7f9fa;
            padding: 15px;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # File uploader for data files
    uploaded_files = st.file_uploader(
        "Upload water quality data files (March 2024 - October 2024)",
        type=["csv"],
        accept_multiple_files=True,
    )

    if not uploaded_files:
        st.info("Please upload CSV files for analysis.")
        return

    # Combine uploaded files into a single DataFrame
    combined_df = pd.DataFrame()
    for file in uploaded_files:
        temp_df = pd.read_csv(file)
        combined_df = pd.concat([combined_df, temp_df], ignore_index=True)

        # Ensure 'Date' or 'Date (MM/DD/YYYY)' column exists and filter for the date range
        # Check for the correct date column
        if 'Date' in combined_df.columns:
            date_column = 'Date'
        elif 'Date (MM/DD/YYYY)' in combined_df.columns:
            date_column = 'Date (MM/DD/YYYY)'
        else:
            st.error("The uploaded data must include a 'Date' or 'Date (MM/DD/YYYY)' column.")
            return

        # Ensure the date column is properly parsed
        combined_df[date_column] = pd.to_datetime(combined_df[date_column], errors='coerce')
        filtered_df = combined_df[
            (combined_df[date_column] >= '2024-03-01') & (combined_df[date_column] <= '2024-10-31')
            ]

        if filtered_df.empty:
            st.warning("No data available for the specified date range.")
            return

        # Rename date column for consistency
        filtered_df = filtered_df.rename(columns={date_column: 'Date'})

    # Focus on the four key parameters
    key_parameters = ['ODO mg/L', 'pH', 'Chlorophyll RFU']
    available_columns = [col for col in key_parameters if col in filtered_df.columns]
    if not available_columns:
        st.error("The uploaded data does not contain the required parameters: ODO mg/L, pH, Chlorophyll RFU.")
        return
    filtered_df = filtered_df[['Date', 'Latitude', 'Longitude', 'Depth m'] + available_columns]

    # Handle invalid depth values (e.g., negative values)
    if 'Depth m' in filtered_df.columns:
        filtered_df = filtered_df[filtered_df['Depth m'] >= 0]  # Filter out negative depths

    # Dropdown for Month Selection
    filtered_df['Month'] = filtered_df['Date'].dt.strftime('%B %Y')
    selected_month = st.selectbox(
        "Select a month to view data:",
        options=filtered_df['Month'].unique(),
    )
    month_data = filtered_df[filtered_df['Month'] == selected_month]

    # Dataframe Preview for Selected Month
    st.markdown(f'<p class="styled-subheader">Dataset for {selected_month}</p>', unsafe_allow_html=True)
    st.dataframe(month_data)

    # Geospatial Depth Visualization
    st.markdown(f'<p class="styled-subheader">Geospatial Depth Visualization</p>', unsafe_allow_html=True)
    st.write(
        "This visualization maps water depth measurements (`Depth m`) across geospatial coordinates, "
        "leveraging the latitude and longitude of sampling locations. The size and color of the markers "
        "indicate the depth values, allowing for easy identification of areas with shallow or deep water."
    )
    st.write(
        "This plot is particularly useful for understanding the distribution of water depths across different "
        "geographical areas. By focusing on specific months, it becomes possible to detect trends or anomalies "
        "in water depth data over time."
    )

    if 'Latitude' in month_data.columns and 'Longitude' in month_data.columns and 'Depth m' in month_data.columns:
        fig = px.scatter_mapbox(
            month_data,
            lat='Latitude',
            lon='Longitude',
            color='Depth m',
            size='Depth m',
            color_continuous_scale="Viridis",
            size_max=15,
            zoom=6,
            mapbox_style="carto-positron",
            title=f"Geo-Depth Map for {selected_month}",
        )
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.warning(
            "The dataset must contain 'Latitude', 'Longitude', and 'Depth m' columns for geospatial visualization.")
    st.markdown('</div>', unsafe_allow_html=True)

    # Monthly Averages Visualization
    st.markdown(f'<p class="styled-subheader">Monthly Averages</p>', unsafe_allow_html=True)
    st.write(
        "This bar chart illustrates the monthly average values for the three key water quality parameters: "
        "`ODO mg/L`, `pH`, and `Chlorophyll RFU`. Aggregated averages provide a high-level view of parameter"
        "variations over time, helping to identify seasonal patterns or consistent trends."
    )
    st.write(
        "By comparing the relative values of different parameters, stakeholders can assess the health of water bodies "
        "and evaluate whether specific months exhibit unusual behavior that warrants further investigation."
    )

    monthly_avg = filtered_df.groupby('Month')[available_columns].mean().reset_index()
    avg_fig = px.bar(
        monthly_avg,
        x='Month',
        y=available_columns,
        title="Key Parameters",
        template="plotly_white",
        barmode='group',
    )
    st.plotly_chart(avg_fig, use_container_width=True)

    # Correlation Heatmap
    st.markdown(f'<p class="styled-subheader">Correlation Heatmap</p>', unsafe_allow_html=True)
    st.write(
        "This heatmap visualizes the correlations between the three key water quality parameters for the selected "
        "month."
        "Positive correlations (closer to 1) indicate that two parameters tend to increase together, while negative "
        "correlations (closer to -1) suggest an inverse relationship."
    )
    st.write(
        "Understanding these relationships is crucial for identifying interdependencies between parameters, which can "
        "inform water quality management strategies. For example, a strong correlation between `pH` and `ODO mg/L` may "
        "point to biochemical processes affecting oxygen levels in the water."
    )

    corr = month_data[available_columns].corr()
    fig, ax = plt.subplots(figsize=(10, 8))
    sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm", ax=ax)
    plt.title(f"Correlation Between Parameters in {selected_month}")
    st.pyplot(fig)
    st.markdown('</div>', unsafe_allow_html=True)

    # Boxplots for Key Parameters
    st.markdown('<h3 class="styled-subheader">Boxplots for Distribution Analysis</h3>', unsafe_allow_html=True)
    st.write(
        "Boxplots provide insights into the distribution of each key parameter, highlighting variability, median values, "
        "and potential outliers. The height of each box represents the interquartile range (IQR), which contains the middle "
        "50% of the data points."
    )
    st.write(
        "Outliers, shown as individual points outside the whiskers, are particularly useful for detecting anomalies in the data. "
        "For instance, extreme values of `Chlorophyll RFU` could indicate localized algal blooms or other environmental events."
    )

    for column in available_columns:
        fig = px.box(
            month_data,
            y=column,
            title=f"Distribution of {column} in {selected_month}",
            template="plotly_white",
            labels={column: column},
        )
        st.plotly_chart(fig, use_container_width=True)

    # Summary of Observations
    st.markdown('<p class="styled-subheader">Summary of Observations</p>', unsafe_allow_html=True)
    st.write(
        f"The analysis focuses on four key parameters: ODO mg/L, pH, Temp ºC, and Chlorophyll RFU, "
        f"providing insights into their trends, relationships, and monthly variations. Additionally, geospatial mapping "
        f"of depth measurements ('Depth m') provides a visual understanding of water depths across different locations."
    )


# Display the selected section
if section == "Data Analysis":
    data_analysis()
elif section == "Predictive Analysis":
    predictive_analysis()
elif section == "Comparative Analysis":
    comparative_analysis()
