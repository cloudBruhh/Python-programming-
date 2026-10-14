import seaborn as sns
import matplotlib.pyplot as plt

sns.set_theme(style="whitegrid")

students = ["Aarav", "Bianca", "Chao", "Divya", "Ethan", "Fatima"]
marks = [78, 92, 65, 88, 71, 95]

colors = sns.color_palette("muted", n_colors=len(students))

plt.figure(figsize=(7, 7))

plt.pie(
    marks,
    labels=students,
    colors=colors,
    autopct="%1.1f%%",
    startangle=90,
    wedgeprops={"edgecolor": "white", "linewidth": 2},
)

plt.title("Distribution of Total Class Marks", fontsize=14, fontweight="bold", pad=20)

plt.tight_layout()
plt.show()
