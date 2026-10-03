import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd

sns.set_theme(style="whitegrid")

data = {
    "Student": ["Aarav", "Bianca", "Chao", "Divya", "Ethan", "Fatima"],
    "Math":     [85, 92, 78, 95, 64, 88],
    "Science":  [90, 96, 72, 98, 60, 85],
    "English":  [78, 88, 80, 92, 70, 82],
    "History":  [82, 85, 75, 90, 68, 80],
    "Art":      [88, 90, 85, 85, 75, 92],
}
df = pd.DataFrame(data)

sns.pairplot(df, hue="Student", diag_kind="kde", palette="muted",
             markers=["o", "s", "D", "^", "v", "p"])

plt.suptitle("Pairwise Subject Correlations", fontsize=14, fontweight="bold", y=1.02)

plt.tight_layout()
plt.show()
