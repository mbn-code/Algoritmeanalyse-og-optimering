import pandas as pd
import numpy as np
import seaborn as sns

import matplotlib.pyplot as plt

def plot_algorithm_comparison(input_filename):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv(input_filename)

    # Ensure that the 'name' column is treated as a string
    data['name'] = data['name'].astype(str)

    # Create a new column to extract the algorithm (Merge Sort or Quick Sort) and size
    data['algorithm'] = data['name'].apply(lambda x: x.split('(')[0].strip())  # Extract 'Merge Sort' or 'Quick Sort'
    data['size'] = data['name'].apply(lambda x: int(x.split('Size: ')[1].split(')')[0]))  # Extract the size

    # Set the plot style
    sns.set_theme(style="whitegrid")

    # Create a figure with 4 subplots
    _, axes = plt.subplots(2, 2, figsize=(14, 12))
    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    # Define categories for easy referencing
    categories = ['Best', 'Average', 'Worst']

    # Function for plotting theoretical complexities
    def plot_theoretical_complexities(ax, x_values, plot_n=True, plot_nlogn=False, plot_n2=False, normalization_factor_n=1, normalization_factor_nlogn=1, normalization_factor_n2=1):
        if plot_n:
            y_n = x_values / normalization_factor_n
            ax.plot(x_values, y_n, label="O(n)", color="blue", linestyle="--", linewidth=2)

        if plot_nlogn:
            y_nlogn = (x_values * np.log(x_values)) / normalization_factor_nlogn
            ax.plot(x_values, y_nlogn, label="O(n log n)", color="black", linestyle="--", linewidth=2)

        if plot_n2:
            y_n2 = (x_values**2) / normalization_factor_n2
            ax.plot(x_values, y_n2, label="O(n^2)", color="grey", linestyle="--", linewidth=2)

    # Loop over the categories (Best, Average, Worst) and plot on separate subplots
    for i, category in enumerate(categories):
        ax = axes[i//2, i%2]

        # Filter data for this category (e.g., Best, Average, Worst)
        category_data = data[data['cat'] == category]

        # Plot measured performance for both algorithms
        sns.lineplot(data=category_data, x="size", y="dur", hue="algorithm", markers=True,
                     palette={"Merge Sort": "orange", "Quick Sort": "purple"}, ax=ax, linewidth=2)

        # Plot theoretical complexities on the same axis
        x_values = np.linspace(min(category_data['size']), max(category_data['size']), 500)
        
        if category == 'Worst':
            plot_theoretical_complexities(ax, x_values, plot_n=True, plot_nlogn=True, plot_n2=True)
        else:
            plot_theoretical_complexities(ax, x_values, plot_n=True, plot_n2=True)

        ax.set_title(f'{category} Case')
        ax.legend()

    plt.show()
