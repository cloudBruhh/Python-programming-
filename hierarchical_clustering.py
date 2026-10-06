import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.cluster.hierarchy import dendrogram, fcluster, linkage
from sklearn.preprocessing import StandardScaler

# 1. Simulate Patient Data (15 Patients, 10 Core Gene Expressions + Cancer Stage)
np.random.seed(42)
patient_ids = [f"Patient_{i:02d}" for i in range(1, 16)]
gene_columns = [f"Gene_{j}" for j in range(1, 11)]

# Create continuous genomic matrix
genomic_matrix = np.random.randn(15, 10)
df = pd.DataFrame(genomic_matrix, columns=gene_columns, index=patient_ids)

# Add clinical categorical cancer stages randomly for this example
stages = ["Stage I", "Stage II", "Stage III", "Stage IV"]
df["Cancer_Stage"] = np.random.choice(stages, size=15)

# 2. Encode Ordinal Cancer Stages to Numbers (Stage I=0, II=1, III=2, IV=3)
stage_mapping = {"Stage I": 0, "Stage II": 1, "Stage III": 2, "Stage IV": 3}
df["Stage_Encoded"] = df["Cancer_Stage"].map(stage_mapping)

# 3. Scale the Combined Data Features
# We include both the scaled genes and the scaled stage rank in the clustering vector
features_to_cluster = gene_columns + ["Stage_Encoded"]
scaler = StandardScaler()
scaled_features = scaler.fit_transform(df[features_to_cluster])

# 4. Calculate Hierarchical Clustering Linkage
# 'ward' linkage minimizes variance within the merging clusters
Z = linkage(scaled_features, method="ward")

# 5. Extract Cluster Assignments (Targeting 3 distinct clinical groups)
df["Hierarchical_Cluster"] = fcluster(Z, t=3, criterion="maxclust")

# 6. Generate the Cross-Tabulation Matrix (Clusters vs. Cancer Stages)
cross_tab = pd.crosstab(df["Hierarchical_Cluster"], df["Cancer_Stage"])
print("--- Patient Distribution: Discovered Clusters vs. True Cancer Stages ---")
print(cross_tab)

# 7. Plot the Clustering Dendrogram
plt.figure(figsize=(10, 6))
dendrogram(
    Z,
    labels=[f"{pid} ({df.loc[pid, 'Cancer_Stage']})" for pid in df.index],
    leaf_rotation=90,
    leaf_font_size=10,
    color_threshold=4.5,  # Visual cut-off line for clusters
)

plt.title(
    "Hierarchical Clustering Dendrogram (Genomics + Cancer Stage Rank)",
    fontsize=13,
    fontweight="bold",
    pad=15,
)
plt.xlabel("Patient ID (True Cancer Stage Field)", fontsize=11)
plt.ylabel("Ward Dissimilarity Distance Linkage", fontsize=11)
plt.axhline(y=4.5, color="r", linestyle="--", label="Cluster Division Cut-off")
plt.legend()
plt.tight_layout()
plt.show()
