import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_algorithm_comparison(input_filename):
    # Load the CSV data into a pandas DataFrame
    data = pd.read_csv(input_filename)

    # Ensure that the 'name' column is treated as a string
    data['name'] = data['name'].astype(str)

    # Create a new column to extract the algorithm (Merge Sort or Quick Sort) and size
    data['algorithm'] = data['name'].apply(lambda x: x.split('(')[0].strip())  # Extract 'Merge Sort' or 'Quick Sort'
    data['size'] = data['name'].apply(lambda x: int(x.split('Size: ')[1].split(')')[0]))  # Extract the size

    # Set the plot style
    sns.set(style="whitegrid")

    # Create a figure with 4 subplots
    fig, axes = plt.subplots(2, 2, figsize=(14, 12))
    plt.subplots_adjust(hspace=0.3, wspace=0.3)

    # Define categories for easy referencing
    categories = ['Best', 'Average', 'Worst']

    # Function for plotting theoretical complexities
    def plot_theoretical_complexities(ax, x_values, plot_nlogn=True, plot_n2=False, normalization_factor_nlogn=1, normalization_factor_n2=1):
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
            # In the Worst case, Merge Sort should have O(n log n), Quick Sort can have O(n^2)
            plot_theoretical_complexities(ax, x_values, plot_nlogn=True, plot_n2=True)
        else:
            # In the Best and Average cases, both algorithms are O(n log n)
            plot_theoretical_complexities(ax, x_values, plot_nlogn=True, plot_n2=False)

        # Set labels, title, and legend for the subplot
        ax.set_title(f'{category} Case Performance', fontsize=14)
        ax.set_xlabel("Problem Size", fontsize=12)
        ax.set_ylabel("Duration (ms)", fontsize=12)
        ax.legend(title="Algorithm", loc="upper left")

    # Separate the worst case plots for Quick Sort and Merge Sort into two separate subplots
    quick_sort_data = data[(data['algorithm'] == 'Quick Sort') & (data['cat'] == 'Worst')]
    merge_sort_data = data[(data['algorithm'] == 'Merge Sort') & (data['cat'] == 'Worst')]

    # Compute normalization factor for O(n^2) scaling
    quick_sort_max_duration = quick_sort_data['dur'].max()
    quick_sort_max_size = quick_sort_data['size'].max()
    normalization_factor_n2 = (quick_sort_max_size**2) / quick_sort_max_duration

    # Quick Sort Worst Case Plot
    ax1 = axes[1, 0]
    sns.lineplot(data=quick_sort_data, x="size", y="dur", color="purple", markers=True, ax=ax1, linewidth=2)
    plot_theoretical_complexities(ax1, x_values, plot_nlogn=False, plot_n2=True, normalization_factor_n2=normalization_factor_n2)
    ax1.set_title('Quick Sort Worst Case Performance', fontsize=14)
    ax1.set_xlabel("Problem Size", fontsize=12)
    ax1.set_ylabel("Duration (ms)", fontsize=12)
    ax1.legend(title="Algorithm", loc="upper left")

    # Merge Sort Worst Case Plot
    ax2 = axes[1, 1]
    sns.lineplot(data=merge_sort_data, x="size", y="dur", color="orange", markers=True, ax=ax2, linewidth=2)
    plot_theoretical_complexities(ax2, x_values, plot_nlogn=True, plot_n2=False)
    ax2.set_title('Merge Sort Worst Case Performance', fontsize=14)
    ax2.set_xlabel("Problem Size", fontsize=12)
    ax2.set_ylabel("Duration (ms)", fontsize=12)
    ax2.legend(title="Algorithm", loc="upper left")

    # Display the plot
    plt.suptitle("Algorithm Performance vs. Theoretical Time Complexities", fontsize=16)
    plt.show()

# Example usage
input_filename = 'src_visualize/results.csv'  # Update this path if needed
plot_algorithm_comparison(input_filename)
