#ifndef TEST_SORTING_H
#define TEST_SORTING_H

#include <iostream>
#include <vector>
#include <cassert>
#include <chrono>
#include <fstream>
#include <algorithm>
#include <random>
#include "sorting.h"

void test_sorting() {
    using namespace std;
    using namespace std::chrono;

    cout << "Running comprehensive sorting algorithm tests..." << endl;

    // Test sizes (increased range for better visualization)
    vector<int> sizes = {100, 500, 1000, 5000, 10000, 20000, 30000, 40000, 50000};
    
    // Open CSV file for writing results
    ofstream csv_file("src_visualize/sorting_results.csv");
    csv_file << "Algorithm,Case,Size,Duration (microseconds)\n";

    // Random number generator for consistent results
    mt19937 rng(42); // Fixed seed for reproducibility

    for (const auto& size : sizes) {
        vector<int> data(size);
        
        // Best Case for Merge Sort (already sorted)
        iota(data.begin(), data.end(), 0);
        {
            auto data_copy = data;
            auto start = high_resolution_clock::now();
            sorting::merge_sort(data_copy);
            auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start).count();
            csv_file << "Merge Sort,Best Case," << size << "," << duration << "\n";
            cout << "Merge Sort (Best Case) size " << size << ": " << duration << " μs\n";
        }

        // Best Case for Quick Sort (random with distinct elements)
        iota(data.begin(), data.end(), 0);
        shuffle(data.begin(), data.end(), rng);
        {
            auto data_copy = data;
            auto start = high_resolution_clock::now();
            sorting::quick_sort(data_copy, 0, data_copy.size() - 1);
            auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start).count();
            csv_file << "Quick Sort,Best Case," << size << "," << duration << "\n";
            cout << "Quick Sort (Best Case) size " << size << ": " << duration << " μs\n";
        }

        // Average Case (random data with duplicates)
        uniform_int_distribution<> dist(0, size/2);
        generate(data.begin(), data.end(), [&]() { return dist(rng); });
        {
            auto data_copy = data;
            auto start = high_resolution_clock::now();
            sorting::merge_sort(data_copy);
            auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start).count();
            csv_file << "Merge Sort,Average Case," << size << "," << duration << "\n";
            cout << "Merge Sort (Average Case) size " << size << ": " << duration << " μs\n";
        }
        {
            auto data_copy = data;
            auto start = high_resolution_clock::now();
            sorting::quick_sort(data_copy, 0, data_copy.size() - 1);
            auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start).count();
            csv_file << "Quick Sort,Average Case," << size << "," << duration << "\n";
            cout << "Quick Sort (Average Case) size " << size << ": " << duration << " μs\n";
        }

        // Worst Case for Merge Sort (reverse sorted)
        iota(data.begin(), data.end(), 0);
        reverse(data.begin(), data.end());
        {
            auto data_copy = data;
            auto start = high_resolution_clock::now();
            sorting::merge_sort(data_copy);
            auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start).count();
            csv_file << "Merge Sort,Worst Case," << size << "," << duration << "\n";
            cout << "Merge Sort (Worst Case) size " << size << ": " << duration << " μs\n";
        }

        // Worst Case for Quick Sort (already sorted - leads to unbalanced partitions)
        iota(data.begin(), data.end(), 0);
        {
            auto data_copy = data;
            auto start = high_resolution_clock::now();
            sorting::quick_sort(data_copy, 0, data_copy.size() - 1);
            auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start).count();
            csv_file << "Quick Sort,Worst Case," << size << "," << duration << "\n";
            cout << "Quick Sort (Worst Case) size " << size << ": " << duration << " μs\n";
        }
    }

    csv_file.close();
    cout << "Sort tests completed! Results written to sorting_results.csv" << endl;
}

#endif // TEST_SORTING_H