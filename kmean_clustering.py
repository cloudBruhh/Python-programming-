import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# 1. Simulate Genomic Data (100 patients, 500 gene expression levels)
np.random.seed(42)
patient_ids = [f"Patient_{i:03d}" for i in range(1, 101)]
gene_columns = [f"Gene_{j}" for j in range(1, 501)]
raw_genomic_matrix = np.random.randn(100, 500)
df_patients = pd.DataFrame(raw_genomic_matrix, columns=gene_columns, index=patient_ids)

# 2. Standardize Features
scaler = StandardScaler()
scaled_data = scaler.fit_transform(df_patients)

# 3. PCA for Dimension Reduction (2D for optimal plotting)
pca_2d = PCA(n_components=2, random_state=42)
reduced_features_2d = pca_2d.fit_transform(scaled_data)
df_plot = pd.DataFrame(
    reduced_features_2d, columns=["PCA_Component_1", "PCA_Component_2"]
)

# 4. Apply K-Means Clustering (K=3 Subtypes)
kmeans_model = KMeans(n_clusters=3, random_state=42, n_init=10)
df_plot["Subtype_Cluster"] = kmeans_model.fit_predict(reduced_features_2d)

# Extract the mathematical center coordinates of Subtypes 0, 1, and 2
centroids = kmeans_model.cluster_centers_

# 5. Generate the K-Means Graph with Centroids
plt.figure(figsize=(9, 6))

# Plot the individual patients
sns.scatterplot(
    x="PCA_Component_1",
    y="PCA_Component_2",
    hue="Subtype_Cluster",
    palette="Set1",
    data=df_plot,
    s=100,
    alpha=0.7,
    edgecolor="w",
)

# Plot the cluster centroids (The "archetypal" patient profiles)
plt.scatter(
    centroids[:, 0],
    centroids[:, 1],
    c="black",
    s=250,
    marker="X",
    label="Subtype Centroids",
    edgecolor="white",
    linewidth=2,
)

# Customize graph details
plt.title(
    "K-Means Cancer Patient Clustering (PCA 2D Projection)",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel(f"PCA Component 1 ({pca_2d.explained_variance_ratio_[0] * 100:.1f}% Variance)")
plt.ylabel(f"PCA Component 2 ({pca_2d.explained_variance_ratio_[1] * 100:.1f}% Variance)")
plt.legend(loc="upper right")
plt.grid(True, linestyle="--", alpha=0.5)

# Render graph
plt.tight_layout()
plt.show()
