import numpy as np
import math
import sklearn as sk
import scipy.stats as st
import sklearn.decomposition as decomp
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec

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





