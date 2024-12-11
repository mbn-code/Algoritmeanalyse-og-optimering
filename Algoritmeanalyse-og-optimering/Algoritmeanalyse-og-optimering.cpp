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
#include <numeric>
#include <random>

void MergeAlg(const std::string& caseType) {
    std::vector<int> data(1000000);
    if (caseType == "Best") {
        std::iota(data.begin(), data.end(), 0); // Best case: already sorted
    }
    else if (caseType == "Worst") {
        std::iota(data.rbegin(), data.rend(), 0); // Worst case: reverse sorted
    }
    else {
        std::generate(data.begin(), data.end(), std::rand); // Average case: random
    }

    InstrumentationTimer timer("Merge Sort", caseType.c_str());
    sorting::merge_sort(data);  // This will be timed by the timer
}

void QuickAlg(const std::string& caseType) {
    std::vector<int> data(1000000);
    if (caseType == "Best") {
        std::iota(data.begin(), data.end(), 0); // Best case: already sorted
    }
    else if (caseType == "Worst") {
        std::iota(data.rbegin(), data.rend(), 0); // Worst case: reverse sorted
    }
    else {
        std::generate(data.begin(), data.end(), std::rand); // Average case: random
    }

    InstrumentationTimer timer("Quick Sort", caseType.c_str());
    sorting::quick_sort(data, 0, data.size() - 1, sorting::PivotStrategy::RANDOM);  // This will be timed by the timer
}


int main() {
    Instrumentor::Get().BeginSession("Sorting Algos");

    {
        MergeAlg("Best");
        QuickAlg("Best");
    }

    {
        MergeAlg("Average");
        QuickAlg("Average");
    }

    {
        MergeAlg("Worst");
        QuickAlg("Worst");
    }

    Instrumentor::Get().EndSession();
    SaveProfilingData("results.json");

    return 0;
}
