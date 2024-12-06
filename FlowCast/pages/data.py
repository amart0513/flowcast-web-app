import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.multioutput import MultiOutputRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from joblib import dump
import os

# Load the dataset
file_path = 'data/oct25-2024.csv'
data = pd.read_csv(file_path)

# Ensure required columns are present
required_features = ['Latitude', 'Longitude', 'Depth m', 'Temp °C', 'pH', 'ODO mg/L']
missing_columns = [col for col in required_features if col not in data.columns]
if missing_columns:
    raise ValueError(f"The dataset is missing required columns: {missing_columns}")

# Prepare features and targets
features = ['Latitude', 'Longitude', 'Depth m', 'Temp °C', 'pH', 'ODO mg/L']
targets = ['Depth m', 'Temp °C', 'pH', 'ODO mg/L']
X = data[features]
y = data[targets]

# Train/test split
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train the multi-output model
multi_output_model = MultiOutputRegressor(RandomForestRegressor(random_state=42))
multi_output_model.fit(X_train, y_train)

# Create the models directory if it doesn't exist
os.makedirs('models', exist_ok=True)

# Save the model
model_path = 'models/multi_output_model.pkl'
dump(multi_output_model, model_path)

# Evaluate the model
y_pred = multi_output_model.predict(X_test)
mse = mean_squared_error(y_test, y_pred, multioutput='raw_values')
overall_mse = mean_squared_error(y_test, y_pred)

# Display evaluation metrics
evaluation_results = pd.DataFrame({
    'Target Variable': targets,
    'Mean Squared Error': mse
})
print(f"Overall MSE: {overall_mse:.5f}")
print(evaluation_results)
