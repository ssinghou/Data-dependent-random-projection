# -*- coding: utf-8 -*-
"""ion_rmsevsk.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1LdSjUhGRKTks6yuYqXjlxtKItPcoqF-N
"""

pip install ucimlrepo

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
from sklearn.random_projection import GaussianRandomProjection
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score
import time

from ucimlrepo import fetch_ucirepo

def compute_rmse(original, reconstructed):
    """Compute the RMSE between the original and reconstructed data."""
    mse = np.mean((original - reconstructed) ** 2)
    rmse = np.sqrt(mse)
    return rmse

# fetch dataset
ionosphere = fetch_ucirepo(id=52)

# data (as pandas dataframes)
X = ionosphere.data.features
y = ionosphere.data.targets

X = X.values
y = y.values.ravel()

k_values = list(range(2, 34))

rmse_ddrp = []
rmse_pca = []

for k in k_values:
    # Original Data-dependent random projection
    n, p = X.shape
    R = np.zeros((p, k))
    for i in range(k):
        beta = np.random.randn(n)
        R[:, i] = X.T @ beta
    T1 = np.matmul(R.T,R)
    T1 = np.linalg.inv(T1)

    T2 = np.matmul(R.T,X.T)
    T2 = np.matmul(T1,T2)

    X_tilde = np.dot(R, T2)
    X_tilde = X_tilde.T

    x_projected_ddrp = X_tilde
    x_reconstructed_ddrp =  x_projected_ddrp @ R
    x_reconstructed_ddrp = x_projected_ddrp
    rmse_ddrp.append(compute_rmse(X, x_reconstructed_ddrp))


    # PCA
    pca = PCA(n_components=k)
    X_projected_pca = pca.fit_transform(X)
    X_reconstructed_pca = pca.inverse_transform(X_projected_pca)
    rmse_pca.append(compute_rmse(X, X_reconstructed_pca))


# Plotting
plt.figure(figsize=(12, 8))
plt.plot(k_values, rmse_ddrp, marker='o', linestyle='-', label="Original Data-Dependent Random Projection")
plt.plot(k_values, rmse_pca, marker='s', linestyle=':', label="PCA")
plt.title('k vs. RMSE for Different Projection Methods')
plt.xlabel('k (Number of Projected Dimensions)')
plt.ylabel('RMSE')
plt.legend()
plt.grid(True)
plt.savefig("extended_v2_rmse_vs_k_comparison.png")
plt.show()