import csv
import matplotlib.pyplot as plt
import numpy as np

# Initialize data structure for algorithms
algorithms = {}

# Read from CSV file
try:
    with open('src_visualize/sorting_results.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            algorithm, size, duration = row
            size = int(size)
            duration = int(duration)
            if algorithm not in algorithms:
                algorithms[algorithm] = {'size': [], 'duration': []}
            algorithms[algorithm]['size'].append(size)
            algorithms[algorithm]['duration'].append(duration)

    # Create plot
    plt.figure(figsize=(12, 8))

    # Plot empirical data
    for algorithm in algorithms:
        sizes = algorithms[algorithm]['size']
        durations = algorithms[algorithm]['duration']
        plt.plot(sizes, durations, marker='o', label=f'{algorithm} (Empirical)', linewidth=2)

    # Calculate proper scale factors
    merge_ratios = []
    quick_ratios = []
    
    for algorithm in algorithms:
        sizes = np.array(algorithms[algorithm]['size'])
        durations = np.array(algorithms[algorithm]['duration'])
        
        if algorithm == "Merge Sort":
            theoretical = sizes * np.log2(sizes)
            merge_ratios.extend(durations / theoretical)
        elif algorithm == "Quick Sort":
            theoretical = sizes * sizes
            quick_ratios.extend(durations / theoretical)

    # Use maximum ratio to ensure theoretical curve stays above empirical data
    merge_scale = max(merge_ratios)
    quick_scale = max(quick_ratios)

    # Plot theoretical complexities
    x = np.linspace(100, 50000, 1000)
    plt.plot(x, merge_scale * x * np.log2(x), '--', label='O(n log n) - Theoretical', alpha=0.5)
    plt.plot(x, quick_scale * x**2, '--', label='O(n²) - Theoretical Worst Case', alpha=0.5)

    plt.xlabel('Input Size (n)')
    plt.ylabel('Duration (microseconds)')
    plt.title('Sorting Algorithm Performance: Empirical vs Theoretical')
    plt.legend()
    plt.grid(True)
    plt.yscale('log')
    plt.xscale('log')

    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print("Error: sorting_results.csv file not found")
except Exception as e:
    print(f"An error occurred: {str(e)}")