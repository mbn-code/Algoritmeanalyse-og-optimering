#include "sorting.h"
#include <filesystem>
#include <fstream>
#include <iostream>
#include <vector>
#include <chrono>
#include <random>
#include <algorithm>

void test_sorting() {
    using namespace std;
    using namespace std::chrono;

    // Ensure the directory exists
    std::filesystem::create_directories("src_visualize");

    cout << "Running comprehensive sorting algorithm tests..." << endl;

    // Test sizes (increased range for better visualization)
    vector<int> sizes = {100, 500, 1000, 5000, 10000, 20000, 30000, 40000, 50000, 100000};

    // Open CSV file for writing results
    ofstream csv_file("src_visualize/sorting_results.csv");
    if (!csv_file.is_open()) {
        cerr << "Error: Could not open file 'src_visualize/sorting_results.csv' for writing.\n";
        return;
    }

    csv_file << "Algorithm,Case,Size,Duration (microseconds)\n";  // Ensure the header is correct

    // Random number generator for consistent results
    mt19937 rng(42); // Fixed seed for reproducibility

    // Set pivot strategy to RANDOM for Average Case
    sorting::set_pivot_strategy(sorting::PivotStrategy::RANDOM);

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
        uniform_int_distribution<> dist(0, size);
        generate(data.begin(), data.end(), [&]() { return dist(rng); });

        // Merge Sort Average Case
        {
            auto data_copy = data;
            auto start = high_resolution_clock::now();
            sorting::merge_sort(data_copy);
            auto duration = duration_cast<microseconds>(high_resolution_clock::now() - start).count();
            csv_file << "Merge Sort,Average Case," << size << "," << duration << "\n";
            cout << "Merge Sort (Average Case) size " << size << ": " << duration << " μs\n";
        }

        // Quick Sort Average Case
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

        // Set pivot strategy to LAST for Worst Case scenario (Quick Sort)
        sorting::set_pivot_strategy(sorting::PivotStrategy::LAST);

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
    if (!csv_file) {
        cerr << "Error closing the file properly.\n";
    } else {
        cout << "Results successfully written to 'src_visualize/sorting_results.csv'.\n";
    }
}
