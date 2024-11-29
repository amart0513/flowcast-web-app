import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error
from joblib import load
import seaborn as sns
import os
import numpy as np

# Page Configuration
st.set_page_config(page_title="FlowCast: Predictions", layout="wide", page_icon="🌊", initial_sidebar_state="expanded")

# Custom CSS for Layout Optimization
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
            margin-bottom: 10px; /* Reduced margin */
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
        }

        /* Section Styling */
        .section-container {
            padding: 20px 50px;
            font-family: 'Monospace', sans-serif;
            background-color: white;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            margin-bottom: 20px; /* Reduced margin */
        }

        /* Subheaders */
        .styled-subheader {
            font-size: 1.5rem;
            font-weight: bold;
            color: #005f73; /* Banner Consistent Color */
            margin-bottom: 10px; /* Reduced margin */
            font-family: 'Monospace', sans-serif;
        }

        /* Tooltips */
        .tooltip {
            font-size: 0.9rem;
            color: gray;
            font-family: 'Monospace', sans-serif;
        }
    </style>
    """,
    unsafe_allow_html=True,
)

# Banner Title
st.markdown('<div class="hero-title">ML Model Prediction for Water Quality</div>', unsafe_allow_html=True)

# Function to Predict Water Quality
def predict_water_quality(df):
    st.markdown('<div class="section-container">', unsafe_allow_html=True)
    st.markdown('<p class="styled-subheader">Model Predictions</p>', unsafe_allow_html=True)

    # Select relevant features for prediction
    features = df[['Depth m', 'Temp °C', 'pH', 'ODO mg/L']]
    st.write("**Features used for prediction**: Depth (m), Temperature (°C), and pH Levels")
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
            plt.clf()  # Clear the figure

            # Error Distribution
            st.markdown('<p class="styled-subheader">Error Distribution</p>', unsafe_allow_html=True)
            errors = true_values - predictions
            plt.figure(figsize=(10, 6))
            sns.histplot(errors, bins=30, kde=True)
            plt.xlabel("Prediction Error (Actual - Predicted ODO mg/L)")
            plt.title("Error Distribution of Predictions")
            st.pyplot(plt)
            plt.clf()  # Clear the figure

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
    st.markdown('</div>', unsafe_allow_html=True)

# Preloaded Dummy Data
def generate_dummy_data():
    data = {
        'Depth m': np.random.uniform(0, 50, 100),
        'Temp °C': np.random.uniform(15, 30, 100),
        'pH': np.random.uniform(7, 8.5, 100),
        'ODO mg/L': np.random.uniform(4, 12, 100)
    }
    return pd.DataFrame(data)

# Main Section
data_toggle = st.radio("Select Data Source", ["Upload CSV File", "Use Preloaded Dummy Data"], help="Choose how to provide data for predictions.")

if data_toggle == "Upload CSV File":
    uploaded_file = st.file_uploader("Upload a CSV file for prediction", type=["csv"])
    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file)
        st.success("File uploaded successfully.")
        predict_water_quality(df)
    else:
        st.warning("Please upload a CSV file to get predictions.")
else:
    st.write("Using preloaded dummy data for predictions.")
    dummy_df = generate_dummy_data()
    st.dataframe(dummy_df.head())
    predict_water_quality(dummy_df)
