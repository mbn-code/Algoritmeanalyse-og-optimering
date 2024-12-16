# Algorithm Analysis and Optimization

[![GitHub Issues](https://img.shields.io/github/issues/mbn-code/Algoritmeanalyse-og-optimering)](https://github.com/mbn-code/Algoritmeanalyse-og-optimering/issues)
[![GitHub Stars](https://img.shields.io/github/stars/mbn-code/Algoritmeanalyse-og-optimering)](https://github.com/mbn-code/Algoritmeanalyse-og-optimering/stargazers)
[![GitHub Forks](https://img.shields.io/github/forks/mbn-code/Algoritmeanalyse-og-optimering)](https://github.com/mbn-code/Algoritmeanalyse-og-optimering/network/members)
[![License](https://img.shields.io/github/license/mbn-code/Algoritmeanalyse-og-optimering)](https://github.com/mbn-code/Algoritmeanalyse-og-optimering/blob/main/LICENSE)

This project focuses on algorithm optimization, analysis, and practical implementations using sorting and searching algorithms. It includes benchmarking and visualization tools to analyze the performance of different algorithms in various scenarios.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running Benchmarks](#running-benchmarks)
  - [Visualizing Sorting Algorithms](#visualizing-sorting-algorithms)
  - [Viewing Profiling Data](#viewing-profiling-data)
- [Detailed Analysis](#detailed-analysis)
- [Results](#results)
- [Conclusion](#conclusion)
- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Questions](#questions)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The aim of this project is to investigate commonly used methods for optimizing algorithms and how these methods are classified. It delves into how mathematics is used to analyze algorithms and their performance, specifically focusing on Merge Sort, Quick Sort, and Binary Search algorithms.

The project stems from the need to understand how algorithm analysis and optimization can save time and computational resources. Algorithms are fundamental in solving problems efficiently, and optimizing them is crucial in practical applications like search engines, data processing, and more.

## Features

- **Sorting Algorithms Implementation**: C++ implementations of Merge Sort and Quick Sort with different pivot strategies.
- **Searching Algorithm Implementation**: C++ implementation of Binary Search.
- **Benchmarking Tool**: Measures the performance of sorting and searching algorithms under Best, Average, and Worst-case scenarios.
- **Visualization**: Python script using `matplotlib` to animate sorting processes.
- **Profiling**: C++ code profiles algorithm performance and outputs the results to JSON files compatible with Chrome Tracing.

## Installation

### Prerequisites

- **C++ Compiler**: Compatible with C++11 or higher (e.g., GCC, Clang, MSVC).
- **Python 3.x**: Along with the following packages:
  - `numpy`
  - `matplotlib`

### Setup Steps

1. **Clone the Repository**

   ```bash
   git clone https://github.com/mbn-code/Algoritmeanalyse-og-optimering.git
   ```

2. **Build the C++ Project**

   - **On macOS/Linux (using Makefile)**

     ```bash
     cd Algoritmeanalyse-og-optimering
     make
     ```

   - **On Windows (using Visual Studio)**

     - Open the solution file in Visual Studio.
     - Build the project from the **Build** menu.

3. **Install Python Dependencies**

   ```bash
   pip install numpy matplotlib
   ```

## Usage

### Running Benchmarks

To run the sorting and searching benchmarks and generate profiling data:

- **Using Visual Studio or Command Line**

  - **Visual Studio**: Build and run the project.
  - **Command Line**: Compile and execute the binary.

- This will execute benchmark tests for varying input sizes and cases.
- Results are saved to `results_sorting.json` and `results_searching.json`.

### Visualizing Sorting Algorithms

To visualize the sorting process:

```bash
python src_visualize/main.py
```

- **Instructions:**
  - You will be prompted to choose the algorithm (`merge` or `quick`).
  - Set the animation speed (seconds per frame).
- **Features:**
  - Animated bar chart of the sorting process.
  - Pseudocode display alongside the visualization with the current line highlighted.
  - Interactive controls to pause/play and navigate through the frames.

### Viewing Profiling Data

The profiling results are saved in JSON format compatible with Chrome Tracing:

1. Open a Chromium-based browser (Chrome, Brave, etc.).
2. Navigate to `chrome://tracing` or `ui.perfetto.dev`.
3. Load the `results_sorting.json` or `results_searching.json` file by dragging and dropping it into the page.
4. Analyze the performance data visually.

## Detailed Analysis

### Sorting Algorithms

- **Quick Sort**: An efficient, in-place sorting algorithm using the divide-and-conquer approach. It selects a 'pivot' element and partitions the array around the pivot. While it has an average-case time complexity of O(n log n), the worst-case performance is O(n²), which occurs when the smallest or largest element is always chosen as the pivot.

- **Merge Sort**: A stable, comparison-based sorting algorithm that consistently performs at O(n log n) time complexity for all cases. It divides the array into halves, sorts them recursively, and then merges the sorted halves. Merge Sort requires additional space proportional to the array size due to the temporary arrays used during the merge process.

### Searching Algorithms

- **Binary Search**: An efficient algorithm for finding an item in a sorted array with a time complexity of O(log n). It repeatedly divides the search interval in half and compares the target value to the middle element. O(1) time complexity can also be reached if lucky and first check of A[mid] == target is true.

## Results

Benchmarking results and profiling data are available for both sorting and searching algorithms.

- **Sorting Results**: [View Sorting Results](Algoritmeanalyse-og-optimering/results_searching.json)
- **Searching Results**: [View Searching Results](Algoritmeanalyse-og-optimering/results_sorting.json)

These JSON files can be loaded into Chrome Tracing for detailed performance analysis.

## Conclusion

In this project, we explored algorithm analysis and optimization, focusing on sorting and searching algorithms. By implementing and benchmarking Quick Sort, Merge Sort, and Binary Search, we gained insights into their performance characteristics in various scenarios. Visualizing the algorithms helped in understanding their behavior and the importance of choosing the right algorithm for a specific problem to optimize time and space complexity.

## Project Overview

**Algorithm analysis and their practical implementations.**

### Objectives

- Analyze and compare the performance of Merge Sort and Quick Sort algorithms.
- Understand how algorithm analysis and optimization can save time and computational resources.
- Demonstrate practical implementations of algorithm optimization techniques.

## Problem Statement

- What is an algorithm?
- How do you analyze an algorithm?
- How can algorithms be analyzed to develop optimized algorithms for practical implementations to save time and computational resources?
- How do you typically calculate and compare time and space complexities in real-world scenarios for algorithms?

## Questions

- What are the most common techniques for algorithm optimization, and how can they be classified?
- How does the choice of data structure affect the efficiency of an algorithm?
- What tools and techniques can be used to benchmark and compare different algorithms?
- How can parallelization and caching be used to improve the performance of existing algorithms?
- What practical examples of algorithm optimization exist in large-scale software projects, and what have been the results? [A1](https://www.henrik-bondtofte.dk/pagerank/)

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for suggestions and improvements.
This project is more than just a project, it's a product and can be used to test any algorithm or instructions to test the time.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
