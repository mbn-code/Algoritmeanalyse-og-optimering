import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Path to the CSV file
csv_file_path = 'src_visualize/results.csv'

# Read CSV data into a DataFrame
df = pd.read_csv(csv_file_path)

# Filter out only the worst-case Quick Sort data
worst_quick_sort = df[df['cat'] == 'Worst']
worst_quick_sort['size'] = worst_quick_sort['name'].str.extract(r'Size: (\d+)')[0].astype(int)
worst_quick_sort['duration'] = worst_quick_sort['dur']

# Print out the unique sizes to ensure we have all expected data points
print("Unique input sizes in the dataset:", worst_quick_sort['size'].unique())

# Print the sizes and durations to debug missing data points
print(worst_quick_sort[['size', 'duration']])

# Plot the data
plt.figure(figsize=(12,8))

# Plot Quick Sort worst-case performance
plt.scatter(worst_quick_sort['size'], worst_quick_sort['duration'], color='red', label='Quick Sort Worst Case', s=100, edgecolors='black')

# Calculate the constant C for O(n^2) based on the largest data point
max_size = max(worst_quick_sort['size'])
max_duration = max(worst_quick_sort['duration'])
C = max_duration / (max_size ** 2)

# Generate the asymptote for O(n^2)
x = np.linspace(min(worst_quick_sort['size']), max(worst_quick_sort['size']), 500)
y_asymptote = C * (x ** 2)

# Plot the asymptote
plt.plot(x, y_asymptote, color='blue', linestyle='--', label=r'$O(n^2)$ Asymptote')

# Add a text annotation for the asymptote
plt.text(max_size * 0.7, C * (max_size ** 2) * 0.8, 'Worst-Case Asymptote: $O(n^2)$', color='blue', fontsize=12, ha='center')

# Labels and Title
plt.xlabel('Input Size (n)', fontsize=14)
plt.ylabel('Time Duration (ms)', fontsize=14)
plt.title('Quick Sort Worst-Case Performance and Asymptote', fontsize=16)

# Displaying the legend
plt.legend(fontsize=12)

# Add grid for better readability
plt.grid(True)

# Show the plot
plt.show()