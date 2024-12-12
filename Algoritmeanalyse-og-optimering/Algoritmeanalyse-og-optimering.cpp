/**
* @file main.cpp
 * @brief Entry point for the application.
 *
 * This file contains the main function which initializes and runs the application.
 *
 * @author Malthe Bang Norengaard
 * @date
 */

 /**
     * @brief Runs the CLI application

     * @details

 **/

 /* ------------------------------- MAIN_CPP ----------------------------------- */

#include "main.h"
#include "sorting.h"
#include <vector>
#include <algorithm>

#include <iostream>
#include <fstream>
#include <numeric>
#include <random>

void RunSortingBenchmarks(int num_runs, int initial_size, int size_increment) {
    Instrumentor::Get().BeginSession("Sorting Benchmarks");

    for (int size = initial_size; size <= initial_size + (num_runs - 1) * size_increment; size += size_increment) {
        std::cout << "Running benchmarks for size: " << size << std::endl;
        for (const std::string& caseType : { "Best", "Average", "Worst" }) {
            std::vector<int> merge_data(size);
            std::vector<int> quick_data = merge_data; // Create a copy for quicksort

            if (caseType == "Best") {
                std::iota(merge_data.begin(), merge_data.end(), 0);
                quick_data = merge_data;
            }
            else if (caseType == "Worst") {
                std::iota(merge_data.rbegin(), merge_data.rend(), 0);
                quick_data = merge_data;
            }
            else {
                std::random_device rd;
                std::mt19937 gen(rd());
                std::uniform_int_distribution<> distrib(0, size * 2); // Adjust range as needed
                std::generate(merge_data.begin(), merge_data.end(), [&]() { return distrib(gen); });
                quick_data = merge_data;
            }

            {
                std::string name = "Merge Sort (" + caseType + ", Size: " + std::to_string(size) + ")";
                InstrumentationTimer timer(name.c_str(), caseType.c_str());
                sorting::merge_sort(merge_data);
            }

            if (caseType == "Best") {
                std::iota(merge_data.begin(), merge_data.end(), 0); // Sorted in ascending order
                quick_data = merge_data;
            }
            else if (caseType == "Worst") {
                std::iota(merge_data.rbegin(), merge_data.rend(), 0); // Sorted in descending order
                quick_data = merge_data;
            }
            else {
                std::random_device rd;
                std::mt19937 gen(rd());
                std::uniform_int_distribution<> distrib(0, size * 2);
                std::generate(merge_data.begin(), merge_data.end(), [&]() { return distrib(gen); });
                quick_data = merge_data;
            }

            // Benchmark Quick Sort with the correct pivot strategy
            {
                std::string name = "Quick Sort (" + caseType + ", Size: " + std::to_string(size) + ")";
                InstrumentationTimer timer(name.c_str(), caseType.c_str());
                if (caseType == "Worst") {
                    sorting::quick_sort(quick_data, 0, quick_data.size() - 1, sorting::PivotStrategy::LAST);
                }
                else {  
                    sorting::quick_sort(quick_data, 0, quick_data.size() - 1, sorting::PivotStrategy::RANDOM);
                }
            }

        }
    }

    Instrumentor::Get().EndSession();
    SaveProfilingData("results.json");
}

int main() {
    RunSortingBenchmarks(3, 100000, 100000); // 5 runs, starting at 100,000, incrementing by 100,000
    return 0;
}