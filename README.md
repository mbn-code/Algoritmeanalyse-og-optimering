# Algorithm Analysis and Optimization

This project focuses on algorithm optimization, analysis, and practical implementations using sorting algorithms. It includes benchmarking and visualization tools to analyze the performance of different sorting algorithms in various scenarios.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Running Benchmarks](#running-benchmarks)
  - [Visualizing Sorting Algorithms](#visualizing-sorting-algorithms)
  - [Plotting Benchmark Results](#plotting-benchmark-results)
- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Questions](#questions)
- [Contributing](#contributing)
- [License](#license)

## Introduction

The aim of this project is to investigate commonly used methods for optimizing algorithms and how these methods are classified. It delves into how mathematics is used to analyze algorithms and their performance, specifically focusing on Merge Sort and Quick Sort algorithms.

## Features

- **Sorting Algorithms Implementation**: C++ implementations of Merge Sort and Quick Sort with different pivot strategies.
- **Benchmarking Tool**: Measures the performance of sorting algorithms under Best, Average, and Worst-case scenarios.
- **Visualization**: Python scripts using `matplotlib` and `seaborn` to animate sorting processes and plot performance data.
- **Data Conversion**: Scripts to convert profiling data between JSON and CSV formats for ease of analysis.
- **Asymptote Analysis**: Tools to calculate and plot asymptotes of functions using `sympy`.

## Installation

### Prerequisites

- **C++ Compiler**: Compatible with C++11 or higher (e.g., GCC, Clang, MSVC).
- **Python 3.x**: Along with the following packages:
  - `numpy`
  - `matplotlib`
  - `pandas`
  - `seaborn`
  - `sympy`

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
     - Download the required C++ tools if prompted.
     - Build the project from the Build menu.

3. **Install Python Dependencies**

   ```bash
   pip install numpy matplotlib pandas seaborn sympy
   ```

## Usage

### Running Benchmarks

To run the sorting benchmarks and generate profiling data:

```bash
Build and Run Visual Studio Project.
```

- This will execute benchmark tests for varying input sizes and cases.
- Results are saved to `results.json`.

### Visualizing Sorting Algorithms

## Multiple Ways Of Displaying Results

To visualize the sorting process in python:

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

### Plotting Benchmark Results

#### Converting JSON to CSV

Convert profiling data for easier analysis:

```bash
python src_visualize/converter.py
```

- Converts `results.json` to `results.csv`.

#### Generating Performance Plots

Plot algorithm performance and compare with theoretical complexities:

```bash
python src_visualize/plotter.py
```

- **Features:**
  - Plots empirical performance data.
  - Overlays theoretical complexity curves (O(n log n), O(n^2)).
  - Separate plots for Best, Average, and Worst-case scenarios.

## Plot Using Chrome Tracing

Plotting with python has it's benefits, but visualizing data with chrome:://tracing also has it's benefits.

To do this do the following steps from earlier, where you run the benchmarker, let it run and generate data with their profiles.
Now we have a results.json file, this file is specifically made to just be dragged and dropped into chrome://tracing
so do that in a chromium based browser like brave or chrome, and you will be able to see the data visualized.

The benefit of this is it's easy and gives great fast detail on the runtime. 

## Project Overview

**Algorithm optimization and their practical implementations.**

### Objectives

- Analyze and compare the performance of Merge Sort and Quick Sort algorithms.
- Understand how algorithm analysis and optimization can save time and computational resources.
- Demonstrate practical implementations of algorithm optimization techniques.

## Problem Statement

- What is an algorithm?
- How do you analyze an algorithm?
- How can algorithms be analyzed to develop optimized algorithms for practical implementations to save time and computational resources?
- How do you typically calculate and compare time and space complexities in real-world scenarios for algorithms?
- What practical software examples demonstrate that algorithm optimization has benefited the project?

## Questions

- What are the most common techniques for algorithm optimization, and how can they be classified?
- How does the choice of data structure affect the efficiency of an algorithm?
- What tools and techniques can be used to benchmark and compare different algorithms?
- How can parallelization and caching be used to improve the performance of existing algorithms?
- What practical examples of algorithm optimization exist in large-scale software projects, and what have been the results?

## Contributing

Contributions are welcome! Please feel free to submit a pull request or open an issue for suggestions and improvements.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
