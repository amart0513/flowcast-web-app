import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from joblib import dump
from joblib import load
import os
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.model_selection import learning_curve

IMAGE_FIU_BANNER = "media/FIU_Banner.png"

st.set_page_config(page_title="FlowCast", layout="wide",
                   page_icon="🌊", initial_sidebar_state="expanded")

with st.sidebar:
    st.title("FlowCast: Sidebar")


    def load_media(column, file_path, caption):
        with column:
            if file_path.endswith(".jpeg") or file_path.endswith(".PNG") or file_path.endswith(".jpg"):
                column.image(file_path, caption=caption, width=200)
            elif file_path.endswith(".mp4"):
                column.video(file_path)
            elif file_path.endswith(".mp3"):
                column.audio(file_path)


    # To make scatter plots
    def scatter_plots(df):
        st.subheader("Scatter Plot")
        fig = px.scatter(df, x="Depth m", y="Temp °C", size="pH", color="ODO mg/L")
        st.plotly_chart(fig)


    # To make map plots
    def maps(df):
        st.subheader("Maps")
        if 'Latitude' in df.columns and 'Longitude' in df.columns:
            fig = px.scatter_mapbox(df, lat="Latitude", lon="Longitude",
                                    hover_data=["Depth m", "pH", "Temp °C", "ODO mg/L"],
                                    zoom=15)
            fig.update_layout(mapbox_style="open-street-map")
            st.plotly_chart(fig)
        else:
            st.error("Missing 'Latitude' or 'Longitude' columns in data.")


    # To make line graphs
    def line_plots(df):
        st.subheader("Line Plot")
        color = st.color_picker("Choose a color", "#081E3F")
        fig = px.line(df, x=df.index, y="ODO mg/L")
        fig.update_traces(line_color=color)
        st.plotly_chart(fig)


    # To make 3D plots
    def three_d_plots(df):
        st.subheader("3D Plot")
        fig = px.scatter_3d(df, x="Longitude", y="Latitude", z="Depth m", color="ODO mg/L")
        fig.update_scenes(zaxis_autorange="reversed")
        st.plotly_chart(fig)


    # Plot the correlation heatmap
    def plot_correlation_heatmap(df):
        plt.figure(figsize=(10, 8))
        sns.heatmap(df.corr(), annot=True, cmap='coolwarm')
        st.pyplot(plt)


    # To make pair plots
    def plot_pairplot(df, target):
        sns.pairplot(df, hue=target)
        st.pyplot(plt)


    # Making predicted vs actual plots
    def plot_predictions_vs_actual(y_test, predictions):
        plt.figure(figsize=(8, 6))
        plt.scatter(y_test, predictions)
        plt.xlabel('Actual')
        plt.ylabel('Predicted')
        plt.title('Predictions vs Actual')
        st.pyplot(plt)


    # Make plot residuals for training model
    def plot_residuals(y_test, predictions):
        residuals = y_test - predictions
        plt.figure(figsize=(8, 6))
        plt.scatter(predictions, residuals)
        plt.axhline(y=0, color='r', linestyle='--')
        plt.xlabel('Predicted')
        plt.ylabel('Residuals')
        plt.title('Residuals Plot')
        st.pyplot(plt)


    # Find the error distribution from model
    def plot_error_distribution(y_test, predictions):
        residuals = y_test - predictions
        plt.figure(figsize=(8, 6))
        sns.histplot(residuals, kde=True)
        plt.title('Distribution of Errors')
        st.pyplot(plt)


    # Make a learning curve plot from the model
    def plot_learning_curve(model, X, y):
        train_sizes, train_scores, test_scores = learning_curve(model, X, y, cv=5)
        train_mean = train_scores.mean(axis=1)
        test_mean = test_scores.mean(axis=1)

        plt.figure(figsize=(8, 6))
        plt.plot(train_sizes, train_mean, label='Training Score')
        plt.plot(train_sizes, test_mean, label='Validation Score')
        plt.xlabel('Training Set Size')
        plt.ylabel('Score')
        plt.title('Learning Curves')
        plt.legend()
        st.pyplot(plt)


    # Raw data from dataframe (csv)
    def raw_data(df):
        st.subheader("Fetched Data")
        st.dataframe(df)
        st.subheader("Descriptive Statistics")
        st.dataframe(df.describe())


def render_data():
    uploaded_file = st.file_uploader("Upload a CSV file", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully.")
    else:
        df = pd.read_csv("mission156-complete.csv")
        st.info("Using default dataset.")

    # Data validation
    required_columns = ['Depth m', 'Temp °C', 'pH', 'ODO mg/L']
    for column in required_columns:
        if column not in df.columns:
            st.error(f"Missing column: {column}. Please upload a valid CSV file.")
            return

    # Handle NaN values
    if df.isnull().values.any():
        st.warning("Data contains NaN values. Please clean your data.")

    st.header("Water Quality Monitoring")
    st.subheader("Data Analysis")

    # Create sliders dynamically based on the data
    min_depth, max_depth = df["Depth m"].min(), df["Depth m"].max()
    min_temp, max_temp = df["Temp °C"].min(), df["Temp °C"].max()
    min_ph, max_ph = df["pH"].min(), df["pH"].max()

    selected_depth = st.slider("Select Depth (m)", min_value=min_depth, max_value=max_depth,
                               value=(min_depth, max_depth))
    selected_temp = st.slider("Select Temperature (°C)", min_value=min_temp, max_value=max_temp,
                              value=(min_temp, max_temp))
    selected_ph = st.slider("Select pH", min_value=min_ph, max_value=max_ph, value=(min_ph, max_ph))

    # Filter data based on user selection
    filtered_df = df[(df["Depth m"].between(selected_depth[0], selected_depth[1])) &
                     (df["Temp °C"].between(selected_temp[0], selected_temp[1])) &
                     (df["pH"].between(selected_ph[0], selected_ph[1]))]

    # Create tabs for different visualizations
    Scatter_Plots_tab, Maps_tab, Line_Plots_tab, threeD_Plots_tab, Raw_Plots_tab = st.tabs(
        ["Scatter Plots", "Maps", "Line", "3D Plots", "Raw Data"])

    # Prepare features and target variable
    features = df[['Depth m', 'Temp °C', 'pH', 'ODO mg/L']]
    target = df['ODO mg/L']

    model_file = 'data.pkl'

    # Model training and metric calculation
    if not os.path.exists(model_file):

        # Plot correlation heatmap
        plot_correlation_heatmap(df)

        # Split data into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.4, random_state=42)

        # Plot learning curve
        plot_learning_curve(model_file, X_train, y_train)

        # Train the model
        model = LinearRegression()
        model.fit(X_train, y_train)

        # Test the model
        predictions = model.predict(X_test)

        # Calculate metrics
        mse = mean_squared_error(y_test, predictions)
        r2 = r2_score(y_test, predictions)

        # Save model
        dump(model, model_file)
        st.success("Model trained and saved.")

    else:
        model = load(model_file)

        # Use filtered data for predictions
        predictions = model.predict(filtered_df[['Depth m', 'Temp °C', 'pH', 'ODO mg/L']])

        # Calculate metrics on filtered data
        mse = mean_squared_error(filtered_df['ODO mg/L'], predictions)
        r2 = r2_score(filtered_df['ODO mg/L'], predictions)

    # Visualization Tabs
    with Scatter_Plots_tab:
        scatter_plots(filtered_df)
    with Maps_tab:
        maps(filtered_df)
    with Line_Plots_tab:
        line_plots(filtered_df)
    with threeD_Plots_tab:
        three_d_plots(filtered_df)
    with Raw_Plots_tab:
        raw_data(filtered_df)


render_data()
