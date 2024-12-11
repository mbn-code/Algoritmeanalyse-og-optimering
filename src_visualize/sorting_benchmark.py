import csv
import matplotlib.pyplot as plt
import numpy as np

# Initialize data structure for algorithms and cases
algorithms = {}

# Read from CSV file
try:
    with open('sorting_results.csv', 'r') as file:
        csv_reader = csv.reader(file)
        next(csv_reader)  # Skip header
        for row in csv_reader:
            algorithm, case, size, duration = row
            size = int(size)
            duration = int(duration)
            key = (algorithm, case)
            if key not in algorithms:
                algorithms[key] = {'size': [], 'duration': []}
            algorithms[key]['size'].append(size)
            algorithms[key]['duration'].append(duration)

    # Create figure with subplots
    fig, (ax1, ax2, ax3) = plt.subplots(1, 3, figsize=(18, 6))
    cases = ['Best Case', 'Average Case', 'Worst Case']
    axes = {case: ax for case, ax in zip(cases, [ax1, ax2, ax3])}
    colors = {'Merge Sort': 'blue', 'Quick Sort': 'red'}

    # Plot data for each case
    for (algorithm, case), data in algorithms.items():
        ax = axes[case]
        sizes = np.array(data['size'])
        durations = np.array(data['duration'])
        
        # Calculate theoretical curves first to scale the constants
        x = np.linspace(min(sizes), max(sizes), 100)
        if algorithm == "Merge Sort":
            # Find scaling factor that keeps all points under the curve
            scale_factor = np.max(durations / (sizes * np.log2(sizes)))
            theoretical_durations = sizes * np.log2(sizes) * scale_factor
            curve_durations = x * np.log2(x) * scale_factor
            ax.plot(x, curve_durations, '--', 
                   color=colors[algorithm], alpha=0.3,
                   label=f'{algorithm} O(n log n)')
        else:
            if case == "Average Case":
                scale_factor = np.max(durations / (sizes * np.log2(sizes)))
                theoretical_durations = sizes * np.log2(sizes) * scale_factor
                curve_durations = x * np.log2(x) * scale_factor
                ax.plot(x, curve_durations, '--',
                       color=colors[algorithm], alpha=0.3,
                       label=f'{algorithm} O(n log n)')
            else:
                scale_factor = np.max(durations / (sizes * sizes))
                theoretical_durations = sizes * sizes * scale_factor
                curve_durations = x * x * scale_factor
                ax.plot(x, curve_durations, '--',
                       color=colors[algorithm], alpha=0.3,
                       label=f'{algorithm} O(n²)')
        
        # Plot empirical data
        ax.plot(sizes, durations, marker='o', 
                label=f'{algorithm}', 
                color=colors[algorithm],
                linewidth=2)
        
        ax.set_title(f'{case}')
        ax.set_xlabel('Input Size (n)')
        ax.set_ylabel('Duration (microseconds)')
        ax.grid(True, alpha=0.3)
        ax.legend()
        ax.set_yscale('log')
        ax.set_xscale('log')

    plt.suptitle('Sorting Algorithm Performance Comparison', y=1.05)
    plt.tight_layout()
    plt.show()

except FileNotFoundError:
    print("Error: sorting_results.csv file not found")
except Exception as e:
    print(f"An error occurred: {str(e)}")