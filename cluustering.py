import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
from sklearn.cluster import AgglomerativeClustering
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

# 3. PCA for Visualization: Force exactly 2 components (2D)
pca_2d = PCA(n_components=2, random_state=42)
reduced_features_2d = pca_2d.fit_transform(scaled_data)

# Create a DataFrame for plotting
df_plot = pd.DataFrame(
    reduced_features_2d, columns=["PCA Component 1", "PCA Component 2"]
)

# 4. Hierarchical Clustering (3 clusters)
clustering_model = AgglomerativeClustering(n_clusters=3, linkage="ward")
df_plot["Subtype_Cluster"] = clustering_model.fit_predict(reduced_features_2d)

# 5. Generate the Cluster Graph
plt.figure(figsize=(9, 6))
sns.scatterplot(
    x="PCA Component 1",
    y="PCA Component 2",
    hue="Subtype_Cluster",
    palette="Set1",
    data=df_plot,
    s=100,  # Marker size
    alpha=0.8,  # Transparency
    edgecolor="w",  # White border around points
)

# Customize the chart look
plt.title(
    "Cancer Patient Subtypes (PCA 2D Projection) example",
    fontsize=14,
    fontweight="bold",
    pad=15,
)
plt.xlabel(
    f"PCA Component 1 ({pca_2d.explained_variance_ratio_[0] * 100:.1f}% Variance)",
    fontsize=11,
)
plt.ylabel(
    f"PCA Component 2 ({pca_2d.explained_variance_ratio_[1] * 100:.1f}% Variance)",
    fontsize=11,
)
plt.legend(title="Discovered Subtypes", loc="upper right")
plt.grid(True, linestyle="--", alpha=0.5)

# Render the graph
plt.tight_layout()
plt.show()
