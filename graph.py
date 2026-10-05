import matplotlib.pyplot as plt
import numpy as np

# 1. Define student data
students = ["Aarav", "Bhuvi", "Chitra", "Divya", "Sudin", "Fatima"]
marks = [78, 92, 65, 88, 71, 95]
colors = ["#2ab7ca", "#fe4a49", "#fed766", "#8d5b4c", "#5dade2", "#a569bd"]

# 2. Calculate average mark
average_mark = np.mean(marks)

# 3. Initialize the plot layout
plt.figure(figsize=(8, 5))

# 4. Create the Bar Chart
# Custom color palette with specific colors for each student bar
bars = plt.bar(students, marks, color=colors, edgecolor="black", alpha=0.85)

# 5. Add an Average Threshold Line
plt.axhline(
    y=float(average_mark),
    color="crimson",
    linestyle="--",
    linewidth=2,
    label=f"Class Average ({average_mark:.1f})",
)

# 6. Annotate the exact marks on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(
        bar.get_x() + bar.get_width() / 2.0,
        height + 1.5,
        f"{height}",
        ha="center",
        va="bottom",
        fontsize=10,
        fontweight="bold",
    )

# 7. Design Customizations
plt.title("Final Examination Performance", fontsize=14, fontweight="bold", pad=15)
plt.xlabel("Student Name", fontsize=12, labelpad=10)
plt.ylabel("Marks Obtained (out of 100)", fontsize=12, labelpad=10)
plt.ylim(0, 110)  # Gives breathing room for the text annotations at the top
plt.grid(axis="y", linestyle=":", alpha=0.6)  # Grid lines only on the horizontal y-axis
plt.legend(loc="lower right")

# 8. Render the visual
plt.tight_layout()
plt.show()
