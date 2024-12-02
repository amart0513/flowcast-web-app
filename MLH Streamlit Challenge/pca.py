import numpy as np
import pandas as pd
import math
import sklearn as sk
import scipy.stats as st
import sklearn.decomposition as decomp
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from math import radians, cos, sin, asin, sqrt
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer


data = pd.read_csv("flowcast-web-app/MLH Streamlit Challenge/mission156-complete.csv")


#normalzing the data before doing anything lol

columns_droped = ['Date (MM/DD/YYYY)', 'Time (HH:mm:ss)']
df1 = data.drop(columns=columns_droped)
df1_mean = df1.mean()
mean_centered_data = df1 - df1_mean
 
#Creating the covariance matrix of the data (aka the features-by-features matrix)
covariance_matrix = np.cov(mean_centered_data, rowvar=False)

#I am going to compute the eigendecomposition 
eigenvalues, eigenvectors = np.linalg.eig(covariance_matrix)
vectors = eigenvectors
eigenValues_into_vectors = np.diag(eigenvalues)
inverse_vectors = np.linalg.inv(vectors)
eigen_decomposition = np.dot(np.dot(vectors, eigenValues_into_vectors), inverse_vectors)


#Sorting the latent factor scores ... placing them by descending order of magnitude
sorting_latent_factors = np.argsort(eigenvalues)[::-1]
nice_eigenvals = eigenvalues[sorting_latent_factors]
nice_eigen_vectors = eigenValues_into_vectors[:,sorting_latent_factors]


#Computing the component scores
compotents =np.dot(df1, nice_eigen_vectors[:, 0:2]) 
factor_scores = (100 * nice_eigenvals) / np.sum(eigenvalues)


#Creating Scree plot to visually determine important variables
# scree plot
fig = plt.figure(figsize=(10,6))
gs = GridSpec(2,4,figure=fig)

ax1 = fig.add_subplot(gs[0,0])
ax1.plot(factor_scores,'ks-',markersize=10)
ax1.set_xlabel('Component index')
ax1.set_ylabel('Percent variance')
ax1.set_title('Scree plot')
ax1.grid()


#Converting lat and longitutde into a single point using Harvestine
columns_droped2 = ['Date (MM/DD/YYYY)', 'Time (HH:mm:ss)', 'Chlorophyll RFU', 'Cond µS/cm', 'Depth m', 'nLF Cond µS/cm', 'ODO % sat', 'ODO % CB', 'ODO mg/L',
                    'Pressure psi a', 'Sal psu', 'SpCond µS/cm', 'TAL PC RFU', 'TDS mg/L', 'Turbidity FNU', 'TSS mg/L',
                    'pH', 'pH mV', 'Temp °C', 'Vertical Position m']
df2 = data.drop(columns=columns_droped2)
print(df2)
def single_pt_haversine(lat, lng, degrees=True):
    """
    'Single-point' Haversine: Calculates the great circle distance
    between a point on Earth and the (0, 0) lat-long coordinate.
    """
    r = 6371  # Earth's radius in kilometers (use 3956 for miles)

    # Convert decimal degrees to radians if 'degrees' is True
    if degrees:
        lat, lng = map(radians, [lat, lng])

    # Haversine formula
    a = sin(lat / 2) ** 2 + cos(lat) * sin(lng / 2) ** 2
    d = 2 * r * asin(sqrt(a))  # Distance in km

    return d

def calculate_distances(df):
    """
    Iterates over a list of (latitude, longitude) coordinates and calculates the
    distance to the origin (0, 0) using the Haversine formula.
    
    :param coords_list: List of tuples, where each tuple contains (latitude, longitude)
    :return: List of distances corresponding to each coordinate in the input list
    """
    distances = []
    
    for index, row  in df2.iterrows():
        lat, lng = row['Latitude'], row['Longitude']
        distance = single_pt_haversine(lat, lng)
        distances.append(distance)
    
    return distances


df2a = calculate_distances(df2)
print(df2a)  

#Changing the time

df3 = data['Time (HH:mm:ss)']
df3 = df3.copy()
def time_to_minutes(time_str):
    hours, minutes, seconds = map(int, time_str.split(':'))
    return hours * 60 + minutes + seconds / 60

# Apply the function to the 'Time' column
df3['Minutes'] = df3.apply(time_to_minutes)
df3a = df3['Minutes']


#Creating the new dataframe
df1['position'] = df2a 

remove_columns = df1[['Latitude', 'Longitude']]
df1 = df1.drop(columns=remove_columns)
df1['minutes'] = df3a
print(df1)

#Re-doing PCA for better results
# Split into training and testing sets
target = df1['ODO mg/L']  # Replace with your target column name
features = df1.drop(columns=['ODO mg/L'])

X_train, X_test, y_train, y_test = train_test_split(features, target, test_size=0.2, random_state=42)

imputer = SimpleImputer(strategy='mean')
X_train_mean = X_train.mean(axis=0)
X_train_std = X_train.std(axis=0)

X_train_standardized = (X_train - X_train_mean) / X_train_std
X_train_imputed = imputer.fit_transform(X_train_standardized)
X_test_standardized = (X_test - X_train_mean) / X_train_std
X_test_imputed = imputer.fit_transform(X_test_standardized)





print(np.isnan(X_train_standardized).sum())
#  PCA
n_components = 8  
pca = PCA(n_components=n_components)

X_train_pca = pca.fit_transform(X_train_imputed )
X_test_pca = pca.transform(X_test_imputed)


print(f"Explained variance ratio by {n_components} components:", pca.explained_variance_ratio_)

regressor = LinearRegression()
regressor.fit(X_train_pca, y_train)

# Predict on test data
y_pred = regressor.predict(X_test_pca)

# Calculate metrics
mse = mean_squared_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)

print(f"Mean Squared Error: {mse}")
print(f"R-squared: {r2}")

X_train_array = X_train.iloc[:, 0].values.reshape(-1, 1)  # Use iloc to select the first column if needed

# Fit the model
model = LinearRegression()
model.fit(X_train_array, y_train)

# Make predictions
y_pred = model.predict(X_train_array)

# Plotting
import matplotlib.pyplot as plt
plt.scatter(X_train_array, y_train, color='blue', label='Data points')
plt.plot(X_train_array, y_pred, color='red', label='Regression Line')
plt.xlabel('Factors')
plt.ylabel('ODO mg/L')
plt.title('Linear Regression')
plt.legend()
plt.show()

# Plot residuals
residuals = y_train - y_pred

plt.scatter(X_train, residuals, color='blue')
plt.hlines(0, X_train.min(), X_train.max(), colors='red', linestyles='dashed')
plt.xlabel('Feature')
plt.ylabel('Residuals')
plt.title('Residuals of Linear Regression')
plt.show()







