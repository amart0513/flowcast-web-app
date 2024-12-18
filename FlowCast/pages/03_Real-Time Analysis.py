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
st.set_page_config(page_title="Combined Analysis", layout="wide", page_icon="🌊")

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
            font-family: "Consolas", monospace;
            animation: fadeIn 1.5s ease-in-out;
        }

        /* Sidebar Styling */
        [data-testid="stSidebar"] {
            background-color: #0a9396; /* Lighter blue from the banner gradient */
            color: white;
            font-family: "Consolas", monospace;
        }

        /* Sidebar Titles */
        [data-testid="stSidebar"] h3 {
            color: white;
            font-weight: bold;
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
            font-family: "Consolas", monospace;
        }

        /* Subheader Styling */
        .styled-subheader {
            font-size: 1.5rem;
            font-weight: bold;
            color: #005f73;
            margin-bottom: 15px;
            font-family: "Consolas", monospace;
        }

        /* Map Container Styling */
        .map-container {
            padding: 20px;
            background-color: rgba(255, 255, 255, 0.95); /* Transparent white */
            border: 2px solid #005f73;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }
        /* Animation */
        @keyframes fadeIn {
            from {
                opacity: 0;
                transform: translateY(20px);
            }
            to {
                opacity: 1;
                transform: translateY(0);
            }
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Banner Title
st.markdown('<div class="hero-title">Combined Analysis</div>', unsafe_allow_html=True)

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
    dataset_toggle = st.radio("Choose Dataset", ["Default Dataset", "Upload Your Own"],
                              help="Select a dataset to analyze.")
    if dataset_toggle == "Upload Your Own":
        uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])
        if uploaded_file:
            df = pd.read_csv(uploaded_file)
            st.success("File uploaded successfully.")
        else:
            st.warning("Please upload a CSV file to proceed.")
            return
    else:
        df = pd.read_csv("data/oct25-2024.csv")
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
            df, x="Longitude", y="Latitude", z="Depth m", color="ODO mg/L",
            color_continuous_scale=px.colors.sequential.ice
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
        st.write("""
        **Explanation**: Displayed below are the predicted and actual values for the water quality metrics: `Depth m`, `Temp °C`, 
        `pH`, and `ODO mg/L`. This comparison provides insights into the model's prediction accuracy.
        """)

        # Select relevant features for prediction
        features = ['Latitude', 'Longitude', 'Depth m', 'Temp °C', 'pH', 'ODO mg/L']
        target_columns = ['Depth m', 'Temp °C', 'pH', 'ODO mg/L']

        if not all(col in df.columns for col in features):
            st.error(
                "The dataset must contain the following columns: Latitude, Longitude, Depth m, Temp °C, pH, ODO mg/L.")
            return

        X = df[features]

        # Load the multi-output model
        model_file = 'models/multi_output_model.pkl'
        if os.path.exists(model_file):
            from joblib import load
            model = load(model_file)

            # Make predictions
            predictions = model.predict(X)
            prediction_df = df.copy()
            for i, col in enumerate(target_columns):
                prediction_df[f'Predicted {col}'] = predictions[:, i]

            st.markdown('<p class="styled-subheader">Predicted Values for All Variables</p>', unsafe_allow_html=True)
            st.dataframe(prediction_df[features + [f'Predicted {col}' for col in target_columns]])

            st.write("""
            **Explanation**: This table shows the input features and model-predicted values for all four target variables: 
            `Depth m`, `Temp °C`, `pH`, and `ODO mg/L`. Compare these predictions with the actual values to evaluate accuracy.
            """)

            # Visualize Predictions for Each Variable
            for actual_col in target_columns:
                predicted_col = f'Predicted {actual_col}'
                st.markdown(f'<p class="styled-subheader">Actual vs Predicted {actual_col}</p>', unsafe_allow_html=True)

                # Scatter Plot
                scatter_fig = px.scatter(
                    x=prediction_df[actual_col],
                    y=prediction_df[predicted_col],
                    labels={"x": f"Actual {actual_col}", "y": f"Predicted {actual_col}"},
                    title=f"Actual vs Predicted {actual_col}",
                    template="plotly_white",
                )
                scatter_fig.add_shape(
                    type="line",
                    x0=prediction_df[actual_col].min(), y0=prediction_df[actual_col].min(),
                    x1=prediction_df[actual_col].max(), y1=prediction_df[actual_col].max(),
                    line=dict(color="Red", dash="dash"),
                )
                st.plotly_chart(scatter_fig, use_container_width=True)

                st.write(f"""
                **Explanation**: This scatter plot compares the actual vs. predicted values for `{actual_col}`. Points closer 
                to the red dashed line indicate better predictions, while points far from the line represent higher errors.
                """)

            # Fish Kill Risk Trends
            st.markdown('<p class="styled-subheader">Fish Kill Risk Trends</p>', unsafe_allow_html=True)

            # Identify critical thresholds for risks
            low_odo_count = prediction_df[prediction_df['Predicted ODO mg/L'] < 4].shape[0]
            high_temp_count = prediction_df[prediction_df['Predicted Temp °C'] > 30].shape[0]
            low_ph_count = prediction_df[prediction_df['Predicted pH'] < 6.5].shape[0]

            st.write(f"🔴 **Low Dissolved Oxygen (< 4 mg/L)**: {low_odo_count} zones")
            st.write(f"🔴 **High Temperature (> 30 °C)**: {high_temp_count} zones")
            st.write(f"🔴 **Low pH (< 6.5)**: {low_ph_count} zones")

            st.write("""
            **Explanation**: These trends highlight how many zones have critical water quality conditions that pose a risk to fish. 
            Low dissolved oxygen is the primary driver of fish kills, while high temperatures and low pH exacerbate stress and mortality.
            """)

            # Map Risk Zones
            st.markdown('<p class="styled-subheader">Fish Kill Risk Zones</p>', unsafe_allow_html=True)
            st.write("""
                            **Explanation**: This map highlights zones where water quality conditions meet critical thresholds for fish kills. 
                            Redder areas indicate greater risk based on low dissolved oxygen levels.
                            """)
            risk_zones = prediction_df[
                (prediction_df['Predicted ODO mg/L'] < 4) |
                (prediction_df['Predicted Temp °C'] > 30) |
                (prediction_df['Predicted pH'] < 6.5)
                ]
            if not risk_zones.empty:
                risk_fig = px.scatter_mapbox(
                    risk_zones,
                    lat="Latitude", lon="Longitude",
                    color="Predicted ODO mg/L",
                    size="Predicted Temp °C",
                    hover_data=["Predicted Depth m", "Predicted pH", "Predicted Temp °C"],
                    color_continuous_scale="reds",
                    mapbox_style="carto-positron",
                    zoom=8,
                    title="Prone Areas to Potential Fish Kills"
                )
                st.plotly_chart(risk_fig, use_container_width=True)
            else:
                st.success("✅ No zones were found with conditions likely to cause fish kills.")

        else:
            st.error(f"Model file {model_file} not found. Train the model first.")

    # Function to Assess Fish Kill Risk
    def predict_fish_kill(df):
        st.markdown('<p class="styled-subheader">Fish Kill Risk Assessment</p>', unsafe_allow_html=True)

        # Select relevant features for prediction
        features = df[['Depth m', 'Temp °C', 'pH', 'ODO mg/L']]
        st.write(
            "**Features used for prediction**: Depth (m), Temperature (°C), pH Levels, and Dissolved Oxygen (ODO mg/L)")
        st.dataframe(features.head())

        # Check if model exists
        model_file = 'models/data.pkl'
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
    data_toggle = st.radio("Select Data Source", ["Upload CSV File", "Use Preloaded Dummy Data"],
                           help="Choose how to provide data for predictions.")

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
    st.markdown('<p class="styled-subheader">Comparative Analysis: March 2024 - October 2024</p>',
                unsafe_allow_html=True)

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
        " Positive correlations (closer to 1) indicate that two parameters tend to increase together, while negative "
        "correlations (closer to -1) suggest an inverse relationship."
    )
    st.write(
        "Understanding these relationships is crucial for identifying interdependencies between parameters, which can "
        "inform water quality management strategies. For example, a strong correlation between `pH` and `ODO mg/L` may "
        "point to biochemical processes affecting oxygen levels in the water."
    )

    corr = month_data[available_columns].corr()

    # Use Plotly for an interactive, scalable heatmap
    fig = px.imshow(
        corr,
        text_auto=".2f",
        color_continuous_scale="icefire",
        labels={"color": "Correlation"},
        title=f"Correlation Between Parameters in {selected_month}",
    )

    # Adjust layout for better scalability
    fig.update_layout(
        autosize=True,
        margin=dict(l=10, r=10, t=40, b=10),
        font=dict(size=10),
    )

    st.plotly_chart(fig, use_container_width=True)

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
