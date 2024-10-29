import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data with 'Fail' values replaced by NaN
data_map_0 = {"Trial": list(range(1, 11)), "Stationary": [113.3, 39.9, 89.2, 50.8, 134.9, 51.3, np.nan, 34.3, np.nan, 168.8], "Moving": [73.2, 79.5, 84.9, 14.9, 55.0, 25.7, 19.3, 68.0, 63.6, 82.5]}
data_map_1 = {"Trial": list(range(1, 11)), "Stationary": [67.28, 22.75, 46.44, 84.39, 37.63, 43.65, 34.11, 71.4, 94.75, 46.78], "Moving": [30.19, 59.4, 36.33, 49.25, 57.34, 40.21, 35.49, 72.66, 17.97, 19.54]}
data_map_2 = {"Trial": list(range(1, 11)), "Stationary": [23.81, 26.22, 25.47, 25.17, 56.5, 29.64, 28.07, 25.91, 62, 29.99], "Moving": [29.1, 64.53, 71.34, 24.25, 23.79, 28.92, 57.7, 35.26, 28.45, 77.31]}
data_map_3 = {"Trial": list(range(1, 11)), "Stationary": [np.nan, np.nan, 131.33, np.nan, 255.93, np.nan, 512.68, np.nan, 349.7, 456.07], "Moving": [110.93, 145.77, 105.02, 57.68, 94.82, 130.18, 75.23, 237.37, 95.48, 132.58]}
data_map_4 = {"Trial": list(range(1, 11)), "Stationary": [143.88, 86.97, np.nan, 375.55, 100.45, 102.7, 135.2, np.nan, 147.8, np.nan], "Moving": [65.54, 99.09, 170.59, 124.77, 44.14, 104.78, 98.83, 92.01, 43.18, 37.42]}

# Convert dictionaries to DataFrames
df_map_0 = pd.DataFrame(data_map_0)
df_map_1 = pd.DataFrame(data_map_1)
df_map_2 = pd.DataFrame(data_map_2)
df_map_3 = pd.DataFrame(data_map_3)
df_map_4 = pd.DataFrame(data_map_4)

# Combine data for box plot
data = [
    df_map_0["Moving"], df_map_0["Stationary"].dropna(),
    df_map_1["Moving"], df_map_1["Stationary"],
    df_map_2["Moving"], df_map_2["Stationary"],
    df_map_3["Moving"], df_map_3["Stationary"].dropna(),
    df_map_4["Moving"], df_map_4["Stationary"].dropna()
]

# Define custom colors as pastel blue and pastel green
colors = ["#AED6F1", "#ABEBC6"]

# Create positions for each map to overlay stationary and moving pairs
positions = [1, 1.3, 2, 2.3, 3, 3.3, 4, 4.3, 5, 5.3]

# Create the box plot with paired boxes touching
fig, ax = plt.subplots(figsize=(12, 8))
box = ax.boxplot(
    data,
    positions=positions,
    patch_artist=True,
    widths=0.3,  # Narrower box width to make pairs appear side by side
    medianprops=dict(color="black", linewidth=2),
    whiskerprops=dict(color="gray", linewidth=1.5),
    capprops=dict(color="gray", linewidth=1.5),
    boxprops=dict(linewidth=1.5)
)

# Set alternating colors for stationary and moving boxes
for i, patch in enumerate(box["boxes"]):
    patch.set_facecolor(colors[i % 2])
    patch.set_edgecolor("gray")
    patch.set_alpha(0.8)

# Update x-axis labels to group by map
ax.set_xticks([1.15, 2.15, 3.15, 4.15, 5.15])  # Centered positions for map labels
ax.set_xticklabels(["Corner", "Middle", "H", "2-Corner", "Crowd"], fontsize=12)

# Title and axis labels
ax.set_title("Completion Times for Stationary and Dynamic Obstacles using Sub-Goals", fontsize=16, fontweight="bold", color="black")
ax.set_ylabel("Time (seconds)", fontsize=14)
ax.set_xlabel("Map", fontsize=14)

# Adding grid for better readability
ax.grid(axis="y", linestyle="--", alpha=0.7)

# Add legend for colors
handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]
labels = ["Dynamic", "Stationary"]
ax.legend(handles, labels, loc="upper right")

plt.subplots_adjust(bottom=0.2)  # Adds space at the bottom for the text

# Display asterisks for significant differences below each pair of boxes
is_sig_dif = [0,0,0,1,0]
for i in range(0, len(positions), 2):
    if is_sig_dif[i // 2] == 1:
        x1, x2 = positions[i], positions[i + 1]
        y = -50
        plt.text((x1 + x2) * 0.5, y + 2, "*", ha="center", va="bottom", color="black", fontsize=14)


# Show plot
plt.tight_layout()
plt.savefig("Exp1_boxplot.png")
plt.show()



# Calculate success rate (non-NaN values / total values) for each condition on each map
success_rates = {
    "Map 1": [df_map_0["Moving"].notna().mean(), df_map_0["Stationary"].notna().mean()],
    "Map 2": [df_map_1["Moving"].notna().mean(), df_map_1["Stationary"].notna().mean()],
    "Map 3": [df_map_2["Moving"].notna().mean(), df_map_2["Stationary"].notna().mean()],
    "Map 4": [df_map_3["Moving"].notna().mean(), df_map_3["Stationary"].notna().mean()],
    "Map 5": [df_map_4["Moving"].notna().mean(), df_map_4["Stationary"].notna().mean()]
}

# Convert success rates to DataFrame
success_df = pd.DataFrame(success_rates, index=["Moving", "Stationary"])

# Plotting the bar plot
fig, ax = plt.subplots(figsize=(10, 6))
success_df.T.plot(kind="bar", color=["#AED6F1", "#ABEBC6"], ax=ax)

ax.set_xticklabels(["Corner", "Middle", "H", "2-Corner", "Crowd"], fontsize=12)


# Customizing the plot
ax.set_title("Success Rate for Stationary and Dynamic Obstacles using Sub-Goals", fontsize=15, fontweight="bold")
ax.set_ylabel("Success Rate", fontsize=14)
ax.set_xlabel("Map", fontsize=14)
ax.set_ylim(0, 1)  # Success rate ranges from 0 to 1
# ax.legend(title="Condition")
ax.grid(axis="y", linestyle="--", alpha=0.7)

labels = ["Dynamic", "Stationary"]
ax.legend(handles, labels, loc="upper right")

# Show plot
plt.tight_layout()
plt.savefig("success_rate_barplot_exp_1.png")
plt.show()