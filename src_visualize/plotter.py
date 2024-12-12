import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = pd.read_csv('src_visualize/results.csv')

# Extract unique sizes and categories
sizes = sorted(set(int(name.split('Size: ')[1].split(')')[0]) for name in data['name']))
categories = data['cat'].unique()

# Initialize a figure
plt.figure(figsize=(12, 8))

# Plot data for each algorithm and category
for algorithm in ['Merge Sort', 'Quick Sort']:
    for category in categories:
        subset = data[(data['name'].str.contains(algorithm)) & (data['cat'] == category)]
        plt.plot(sizes, subset['dur'], label=f'{algorithm} ({category})')

# Add O(n log n) asymptote
n = np.array(sizes)
plt.plot(n, n * np.log(n), 'k--', label='O(n log n)')

# Add titles and labels
plt.title('Sorting Algorithm Performance with O(n log n) Asymptote')
plt.xlabel('Input Size')
plt.ylabel('Duration (ns)')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

# Initialize a figure for Quick Sort worst case
plt.figure(figsize=(12, 8))

# Plot data for Quick Sort worst case
for category in categories:
    if category == 'Worst':
        subset = data[(data['name'].str.contains('Quick Sort')) & (data['cat'] == category)]
        plt.plot(sizes, subset['dur'], label=f'Quick Sort ({category})')

# Add O(n^2) asymptote
plt.plot(n, n**2, 'r--', label='O(n^2)')

# Add titles and labels
plt.title('Quick Sort Worst Case Performance with O(n^2) Asymptote')
plt.xlabel('Input Size')
plt.ylabel('Duration (ns)')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()
