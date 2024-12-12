import numpy as np
import matplotlib.pyplot as plt
import json

def extract_data(filename):
    """
    Extracts sorting algorithm performance data from a JSON file.

    Args:
        filename: Path to the JSON file containing the data.

    Returns:
        Tuples of lists containing size and duration for each sorting algorithm and case:
            - merge_sort_best
            - merge_sort_avg
            - merge_sort_worst
            - quick_sort_best
            - quick_sort_avg
            - quick_sort_worst
            - sizes: List of input sizes.
    """
    with open(filename, 'r') as f:
        data = json.load(f)

    merge_sort_best = []
    merge_sort_avg = []
    merge_sort_worst = []
    quick_sort_best = []
    quick_sort_avg = []
    quick_sort_worst = []
    sizes = []

    for event in data["traceEvents"]:
        size_str = event["name"].split("Size: ")[1].rstrip(")")
        size = int(size_str)
        if "Merge Sort" in event["name"]:
            if "Best" in event["name"]:
                merge_sort_best.append((size, event["dur"]))
            elif "Average" in event["name"]:
                merge_sort_avg.append((size, event["dur"]))
            else:
                merge_sort_worst.append((size, event["dur"]))
        else:
            if "Best" in event["name"]:
                quick_sort_best.append((size, event["dur"]))
            elif "Average" in event["name"]:
                quick_sort_avg.append((size, event["dur"]))
            else:
                quick_sort_worst.append((size, event["dur"]))
        sizes.append(size)

    return merge_sort_best, merge_sort_avg, merge_sort_worst, \
           quick_sort_best, quick_sort_avg, quick_sort_worst, sizes

def plot_data(merge_sort_best, merge_sort_avg, merge_sort_worst, 
              quick_sort_best, quick_sort_avg, quick_sort_worst, sizes):
    """
    Plots the performance of sorting algorithms.

    Args:
        merge_sort_best, merge_sort_avg, merge_sort_worst, 
        quick_sort_best, quick_sort_avg, quick_sort_worst, sizes: 
            Data extracted from the JSON file.
    """
    plt.figure(figsize=(12, 8))

    # Unpack size and duration from each tuple
    size_best, duration_best = zip(*merge_sort_best)
    size_avg, duration_avg = zip(*merge_sort_avg)
    size_worst, duration_worst = zip(*merge_sort_worst)
    quick_size_best, quick_duration_best = zip(*quick_sort_best)
    quick_size_avg, quick_duration_avg = zip(*quick_sort_avg)
    quick_size_worst, quick_duration_worst = zip(*quick_sort_worst)

    # Plot Merge Sort
    plt.plot(size_best, duration_best, label="Merge Sort Best Case")
    plt.plot(size_avg, duration_avg, label="Merge Sort Average Case")
    plt.plot(size_worst, duration_worst, label="Merge Sort Worst Case")

    # Plot Quick Sort
    plt.plot(quick_size_best, quick_duration_best, label="Quick Sort Best Case")
    plt.plot(quick_size_avg, quick_duration_avg, label="Quick Sort Average Case")
    plt.plot(quick_size_worst, quick_duration_worst, label="Quick Sort Worst Case")

    # Calculate O(n^2) values
    sizes_squared = [x * x for x in sizes]

    # Plot O(n^2) line
    plt.plot(sizes, sizes_squared, label="O(n^2)")

    # Customize plot
    plt.xlabel("Input Size")
    plt.ylabel("Runtime (ns)")
    plt.title("Sorting Algorithm Comparison")
    plt.legend()
    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    merge_sort_best, merge_sort_avg, merge_sort_worst, \
    quick_sort_best, quick_sort_avg, quick_sort_worst, sizes = \
        extract_data("src_visualize/results.json") 
    plot_data(merge_sort_best, merge_sort_avg, merge_sort_worst, 
              quick_sort_best, quick_sort_avg, quick_sort_worst, sizes)