#ifndef TEST_SORTING_H
#define TEST_SORTING_H

#include <iostream>
#include <vector>
#include <cassert>
#include <chrono>
#include <fstream>
#include "sorting.h"

void test_sorting() {
    using namespace std;
    using namespace std::chrono;

    cout << "Running sort tests..." << endl;

    vector<int> sizes = {100, 500, 1000, 5000, 10000, 20000, 30000, 40000, 50000};
    vector<string> algorithms = {"Merge Sort", "Quick Sort"};

    ofstream csv_file("sorting_results.csv");
    csv_file << "Algorithm,Size,Duration (microseconds)\n";

    for (const auto& size : sizes) {
        vector<int> data(size);
        generate(data.begin(), data.end(), rand);

        for (const auto& algo : algorithms) {
            vector<int> data_copy = data;
            auto start = high_resolution_clock::now();

            if (algo == "Merge Sort") {
                sorting::merge_sort(data_copy);
            } else if (algo == "Quick Sort") {
                sorting::quick_sort(data_copy, 0, data_copy.size() - 1);
            }

            auto end = high_resolution_clock::now();
            auto duration = duration_cast<microseconds>(end - start).count();
            cout << algo << " with size " << size << " took " << duration << " microseconds" << endl;
            csv_file << algo << "," << size << "," << duration << "\n";
        }
    }

    csv_file.close();
    cout << "Sort tests completed!" << endl;
}

#endif // TEST_SORTING_H
