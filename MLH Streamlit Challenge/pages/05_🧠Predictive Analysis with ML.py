import streamlit as st
import pandas as pd
from matplotlib import pyplot as plt
from sklearn.metrics import mean_squared_error, r2_score
from joblib import load
import os
import seaborn as sns

IMAGE_FIU_BANNER = "media/FIU_Banner.png"

st.set_page_config(page_title="FlowCast: Title", layout="wide",
                   page_icon="🌊", initial_sidebar_state="expanded")



def predict_water_quality(df):
    # Select relevant features for prediction
    features = df[['Depth m', 'Temp °C', 'pH', 'ODO mg/L']]
    st.write("**Features used for prediction**: Depth of EXO 2 to Ocean Surface, Temperature in Celsius, and pH Levels "
             "in the Ocean", features.head())

    # Check if model exists
    model_file = 'data.pkl'
    if os.path.exists(model_file):
        model = load(model_file)

        # Make predictions
        predictions = model.predict(features)

        # Display predictions
        st.subheader("Predicted Dissolved Oxygen (ODO mg/L)")
        prediction_df = df.copy()
        prediction_df['Predicted ODO mg/L'] = predictions
        st.dataframe(prediction_df[['Depth m', 'Temp °C', 'pH', 'Predicted ODO mg/L']])

        if 'ODO mg/L' in df.columns:
            true_values = df['ODO mg/L']
            mse = mean_squared_error(true_values, predictions)
            st.write(f"**Mean Squared Error (MSE):** {mse}")

            # Scatter Plot
            st.subheader("Actual vs Predicted Dissolved Oxygen (ODO mg/L)")
            plt.figure(figsize=(10, 6))
            plt.scatter(true_values, predictions, alpha=0.6)
            plt.plot([true_values.min(), true_values.max()], [true_values.min(), true_values.max()], 'r--', lw=2)
            plt.xlabel("Actual ODO mg/L")
            plt.ylabel("Predicted ODO mg/L")
            plt.title("Scatter Plot of Actual vs Predicted ODO")
            st.pyplot(plt)
            plt.clf()  # Clear the figure

            # Error Distribution
            # calculating residuals...
            st.subheader("Error Distribution")
            errors = true_values - predictions
            plt.figure(figsize=(10, 6))
            sns.histplot(errors, bins=30, kde=True)
            plt.xlabel("Prediction Error (Actual - Predicted ODO mg/L)")
            plt.title("Error Distribution of Predictions")
            st.pyplot(plt)
            plt.clf()  # Clear the figure

            # Line Plot
            # suggestion: create a line with residuals, add more "info" into the graph to explain the differences in the
            # water quality...
            st.subheader("Line Plot of Actual and Predicted ODO over Index")
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


st.title("ML Model Prediction for Water Quality")
uploaded_file = st.file_uploader("Upload a CSV file for prediction", type=["csv"])

if uploaded_file is not None:
    # Load the uploaded file
    df = pd.read_csv(uploaded_file)
    st.success("File uploaded successfully")

    # Run the prediction function
    predict_water_quality(df)

else:
    st.warning("Please upload a CSV file to get predictions.")



# maybe create a way to just have sav files already in the system instead of user based interaction with the program
# suggestion: randomize all csv files (maybe create dummy data)