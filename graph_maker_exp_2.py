import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Data with 'Fail' values replaced by NaN
# Data for first map
data_map_0 = {
    "Sub-Goals": [73.2, 79.5, 84.9, 14.9, 55.0, 25.7, 19.3, 68.0, 63.6, 82.5],
    "No Sub-Goals": [17.9, 19.5, 19.6, 18.3, 17.1, 19.4, 18.5, 17.8, 19.8, 16.1]
}
# Data for second map
data_map_1 = {
    "Sub-Goals": [30.19, 59.4, 36.33, 49.25, 57.34, 40.21, 35.49, 72.66, 17.97, 19.54],
    "No Sub-Goals": [19.54, 20.66, 39.19, 29.59, 34.5, 35.27, 21.49, 21.08, 21.83, 22.38]
}
# Data for third map
data_map_2 = {
    "Sub-Goals": [29.1, 64.53, 71.34, 24.25, 23.79, 28.92, 57.7, 35.26, 28.45, 77.31],
    "No Sub-Goals": [109.62, 28.53, 100.62, 30.54, 362.69, 71.63, 111.39, 27.06, 23.07, 33.02]
}
# Data for fourth map
data_map_3 = {
    "Sub-Goals": [110.93, 145.77, 105.02, 57.68, 94.82, 130.18, 75.23, 237.37, 95.48, 132.58],
    "No Sub-Goals": [206.52, 195.37, 200.51, 367.35, np.nan, 179.58, 194.25, 237.28, 167.96, 131.02]
}
# Data for fifth map
data_map_4 = {
    "Sub-Goals": [65.54, 99.09, 170.59, 124.77, 44.14, 104.78, 98.83, 92.01, 43.18, 37.42],
    "No Sub-Goals": [59.19, 37.00, 28.64, 54.60, 51.29, 41.14, 42.03, 30.37, 24.79, 30.75]
}

# Convert dictionaries to DataFrames
df_map_0 = pd.DataFrame(data_map_0)
df_map_1 = pd.DataFrame(data_map_1)
df_map_2 = pd.DataFrame(data_map_2)
df_map_3 = pd.DataFrame(data_map_3)
df_map_4 = pd.DataFrame(data_map_4)

# Combine data for box plot
data = [
    df_map_0["Sub-Goals"], df_map_0["No Sub-Goals"],
    df_map_1["Sub-Goals"], df_map_1["No Sub-Goals"],
    df_map_2["Sub-Goals"], df_map_2["No Sub-Goals"],
    df_map_3["Sub-Goals"], df_map_3["No Sub-Goals"].dropna(),
    df_map_4["Sub-Goals"], df_map_4["No Sub-Goals"]
]

# Define custom colors as pastel blue and pastel purple
colors = ["#AED6F1", "#D7BDE2"]

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
ax.set_title("Completion Time for Sub-Goal and Non Sub-Goal Forming Agents with Dynamic Obstacles", fontsize=16, fontweight="bold", color="black")
ax.set_ylabel("Time (seconds)", fontsize=14)
ax.set_xlabel("Map", fontsize=14)

# Adding grid for better readability
ax.grid(axis="y", linestyle="--", alpha=0.7)

# Add legend for colors
handles = [plt.Line2D([0], [0], color=color, lw=4) for color in colors]
labels = ["Sub-Goals", "No Sub-Goals"]
ax.legend(handles, labels, loc="upper right")

plt.subplots_adjust(bottom=0.2)  # Adds space at the bottom for the text

# Display asterisks for significant differences below each pair of boxes
is_sig_dif = [1,1,0,1,1]
for i in range(0, len(positions), 2):
    if is_sig_dif[i // 2] == 1:
        x1, x2 = positions[i], positions[i + 1]
        y = -32
        plt.text((x1 + x2) * 0.5, y + 2, "*", ha="center", va="bottom", color="black", fontsize=14)

# Show plot
plt.tight_layout()
plt.savefig("Exp2_boxplot.png")
plt.show()

# Calculate success rate (non-NaN values / total values) for each condition on each map
success_rates = {
    "Map 1": [df_map_0["Sub-Goals"].notna().mean(), df_map_0["No Sub-Goals"].notna().mean()],
    "Map 2": [df_map_1["Sub-Goals"].notna().mean(), df_map_1["No Sub-Goals"].notna().mean()],
    "Map 3": [df_map_2["Sub-Goals"].notna().mean(), df_map_2["No Sub-Goals"].notna().mean()],
    "Map 4": [df_map_3["Sub-Goals"].notna().mean(), df_map_3["No Sub-Goals"].notna().mean()],
    "Map 5": [df_map_4["Sub-Goals"].notna().mean(), df_map_4["No Sub-Goals"].notna().mean()]
}

# Convert success rates to DataFrame
success_df = pd.DataFrame(success_rates, index=["Sub-Goals", "No Sub-Goals"])

# Plotting the bar plot
fig, ax = plt.subplots(figsize=(10, 6))
success_df.T.plot(kind="bar", color=["#AED6F1", "#D7BDE2"], ax=ax)

ax.set_xticklabels(["Corner", "Middle", "H", "2-Corner", "Crowd"], fontsize=12)


# Customizing the plot
ax.set_title("Success Rate for Sub-Goal and Non Sub-Goal Agents with Dynamic Obstacles", fontsize=15, fontweight="bold")
ax.set_ylabel("Success Rate", fontsize=14)
ax.set_xlabel("Map", fontsize=14)
ax.set_ylim(0, 1)  # Success rate ranges from 0 to 1
ax.legend()
ax.grid(axis="y", linestyle="--", alpha=0.7)

# Show plot
plt.tight_layout()
plt.savefig("success_rate_barplot_exp_2.png")
plt.show()