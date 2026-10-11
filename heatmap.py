import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

sns.set_theme(style="whitegrid")

data = {
    "Student": ["Aarav", "Bianca", "Chao", "Divya", "Ethan", "Fatima"],
    "Math": [85, 92, 78, 95, 64, 88],
    "Science": [90, 96, 72, 98, 60, 85],
    "English": [78, 88, 80, 92, 70, 82],
    "History": [82, 85, 75, 90, 68, 80],
    "Art": [88, 90, 85, 85, 75, 92],
}
df = pd.DataFrame(data).set_index("Student")

plt.figure(figsize=(8, 5))
sns.heatmap(
    df,
    annot=True,
    fmt="d",
    cmap="RdYlGn",
    linewidths=0.5,
    linecolor="white",
    cbar_kws={"label": "Marks"},
)

plt.title("Student Performance Across Subjects", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Subject")
plt.ylabel("Student")

plt.tight_layout()
plt.show()
