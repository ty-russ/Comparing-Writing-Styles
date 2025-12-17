import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.stats import f_oneway

# Load data
csv_path = "merged_pos_outfit_v2.csv"
try:
    df = pd.read_csv(csv_path)
except FileNotFoundError:
    print(f"Error: {csv_path} not found.")
    exit(1)

# Filter for US and Europe
target_classes = ['us', 'europe']
df_filtered = df[df['Class'].isin(target_classes)].copy()

# Variables to analyze
metrics = ['polarity', 'subjectivity']

# Set up the plot
fig, axes = plt.subplots(1, 2, figsize=(14, 6))
sns.set_theme(style="whitegrid")

for i, metric in enumerate(metrics):
    ax = axes[i]
    
    # Statistical Test (ANOVA, which is equivalent to t-test for 2 groups)
    # Allows for "Tukey-like" logic: if sig -> different letters, else same.
    group1 = df_filtered[df_filtered['Class'] == 'us'][metric]
    group2 = df_filtered[df_filtered['Class'] == 'europe'][metric]
    
    # Drop NaNs just in case
    group1 = group1.dropna()
    group2 = group2.dropna()
    
    f_stat, p_val = f_oneway(group1, group2)
    
    # Significance logic for letters (Tukey style)
    # If p < 0.05, they are different groups (a, b)
    # If p >= 0.05, they are effectively the same group (a, a)
    if p_val < 0.05:
        letters = {'us': 'a', 'europe': 'b'}
        sig_text = f"Significant difference\n(p={p_val:.2e})"
    else:
        letters = {'us': 'a', 'europe': 'a'}
        sig_text = f"No significant difference\n(p={p_val:.2f})"

    # Box Plot
    sns.boxplot(x='Class', y=metric, data=df_filtered, ax=ax, hue='Class', palette="Set2", legend=False)
    ax.set_title(f'{metric.capitalize()} by Region', fontsize=14, fontweight='bold')
    
    # Annotate with letters
    # Get y-axis limit to place letters above the max of each group
    y_max = df_filtered[metric].max()
    offset = y_max * 0.05 # 5% offset
    
    # Get positions (0 and 1)
    # Note: Seaborn's boxplot order matches the unique values or the 'order' param.
    # By default, it sorts alphabetically or appearance. Let's fix order to be safe.
    order = ['europe', 'us'] # Alphabetical usually default
    # Redraw to ensure order, though ax is already drawn on. 
    # Actually, better to just draw once with correct order.
    # Clearing axis to redraw cleanly or just drawing once correctly above.
    ax.clear()
    sns.boxplot(x='Class', y=metric, data=df_filtered, ax=ax, hue='Class', palette="Set2", order=order, legend=False)
    ax.set_title(f'{metric.capitalize()} by Region', fontsize=14, fontweight='bold')
    
    for j, region in enumerate(order):
        # Find max value for this region to place text
        region_vals = df_filtered[df_filtered['Class'] == region][metric]
        if not region_vals.empty:
            region_max = region_vals.max()
            ax.text(j, region_max + offset, letters[region], 
                    ha='center', va='bottom', fontsize=14, fontweight='bold', color='black')

    # Add p-value text to plot
    ax.text(0.5, 1.05, sig_text, transform=ax.transAxes, ha='center', fontsize=10, color='darkred')

plt.tight_layout()
plt.show()
