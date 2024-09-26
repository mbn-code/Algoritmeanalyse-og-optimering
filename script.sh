#!/bin/bash

# Define the project root directory
PROJECT_ROOT="project-root"

# Create the directory structure
mkdir -p $PROJECT_ROOT/{src,include,tests,data,docs}

# Create placeholder files
touch $PROJECT_ROOT/src/{main.cpp,algorithm_optimization.cpp,algorithm_analysis.cpp,benchmark.cpp}
touch $PROJECT_ROOT/include/{algorithm_optimization.h,algorithm_analysis.h,benchmark.h}
touch $PROJECT_ROOT/tests/{test_algorithm_optimization.cpp,test_algorithm_analysis.cpp,test_benchmark.cpp}
touch $PROJECT_ROOT/data/sample_data.txt
touch $PROJECT_ROOT/docs/{README.md,report.md}
touch $PROJECT_ROOT/CMakeLists.txt
touch $PROJECT_ROOT/Makefile

echo "Project structure created successfully."