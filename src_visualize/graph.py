import numpy as np

import matplotlib.pyplot as plt

# Generate data
n = np.linspace(1, 100, 100)
log_n = np.log2(n)
n_log_n = n * log_n
n_squared = n**2
n_linear = n

# Set up plot
plt.figure(figsize=(10, 6))

# Plot the lines
plt.plot(n, log_n, label="Binary Search O(log n)", color='green', linewidth=2)
plt.plot(n, n_log_n, label="QuickSort/MergeSort O(n log n)", color='blue', linewidth=2)
plt.plot(n, n_squared, label="BubbleSort/QuickSort Worst O(n^2)", color='red', linewidth=2)
plt.plot(n, n_linear, label="Linear O(n)", color='orange', linewidth=2)

# Add labels and title
plt.xlabel("Input Size (n)", fontsize=12)
plt.ylabel("Number of Operations", fontsize=12)
plt.title("Time Complexities of Algorithms", fontsize=14)

# Add legend
plt.legend(fontsize=10)

# Add grid
plt.grid(True, linestyle='--', alpha=0.5)

# Show the plot
plt.show()
