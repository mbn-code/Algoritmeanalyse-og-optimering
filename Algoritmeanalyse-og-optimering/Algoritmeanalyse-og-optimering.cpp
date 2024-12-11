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
#include <chrono>
#include <iostream>
#include <fstream>
#include <random>


void save_results(const std::string& filename, const std::string& case_type, const std::string& algorithm, double duration) {
    std::ofstream file(filename, std::ios::app);
    if (file.is_open()) {
        file << case_type << " case for " << algorithm << ": " << duration << " ms" << std::endl;
        file.close();
    }
}

double measure_sort_time(void(*sort_func)(std::vector<int>&), std::vector<int>& data) {
    auto start = std::chrono::high_resolution_clock::now();
    sort_func(data);
    auto end = std::chrono::high_resolution_clock::now();
    std::chrono::duration<double, std::milli> duration = end - start;
    return duration.count();
}

void test_sorting_algorithm(const std::string& algorithm_name, void(*sort_func)(std::vector<int>&), const std::vector<int>& dataset) {
    std::vector<int> best_case = dataset;
    std::vector<int> average_case = dataset;
    std::vector<int> worst_case = dataset;

    // Best case
    std::sort(best_case.begin(), best_case.end());
    double best_case_time = measure_sort_time(sort_func, best_case);
    save_results(algorithm_name + "_results.txt", "Best", algorithm_name, best_case_time);

    // Average case
    double total_average_case_time = 0.0;
    std::random_device rd;
    std::mt19937 g(rd());
    for (int i = 0; i < 10; ++i) {
        std::shuffle(average_case.begin(), average_case.end(), g);
        total_average_case_time += measure_sort_time(sort_func, average_case);
    }
    double average_case_time = total_average_case_time / 10;
    save_results(algorithm_name + "_results.txt", "Average", algorithm_name, average_case_time);

    // Worst case
    std::sort(worst_case.begin(), worst_case.end());
    double worst_case_time = measure_sort_time(sort_func, worst_case);
    save_results(algorithm_name + "_results.txt", "Worst", algorithm_name, worst_case_time);
}

#include <numeric> // Add this include for std::iota

int main() {
    Instrumentor::Get().BeginSession("Session Name");

    {
        InstrumentationTimer timer("Profiled Scope Name", "Best");

        // Define larger datasets
        std::vector<int> dataset1(1000);
        std::vector<int> dataset2(10000);
        std::vector<int> dataset3(100000);

        std::iota(dataset1.begin(), dataset1.end(), 1);
        std::iota(dataset2.begin(), dataset2.end(), 1);
        std::iota(dataset3.begin(), dataset3.end(), 1);

        // Test merge sort
        test_sorting_algorithm("Merge Sort", sorting::merge_sort, dataset1);
        test_sorting_algorithm("Merge Sort", sorting::merge_sort, dataset2);
        test_sorting_algorithm("Merge Sort", sorting::merge_sort, dataset3);

        // Test quick sort
        auto quick_sort_wrapper = [](std::vector<int>& arr) {
            sorting::quick_sort(arr, 0, arr.size() - 1);
        };
        test_sorting_algorithm("Quick Sort", quick_sort_wrapper, dataset1);
        test_sorting_algorithm("Quick Sort", quick_sort_wrapper, dataset2);
        test_sorting_algorithm("Quick Sort", quick_sort_wrapper, dataset3);
    }

    Instrumentor::Get().EndSession();
    SaveProfilingData("results.json");

    return 0;
}
