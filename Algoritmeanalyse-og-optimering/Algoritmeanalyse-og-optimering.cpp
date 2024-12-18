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

#pragma comment(lib, "raylib.lib")
#pragma comment(lib, "winmm.lib")

/**
 * @brief Function to run sorting algorithm benchmarks.
 *
 * @param num_runs Number of test runs for benchmarking.
 * @param initial_size Initial size of the dataset.
 * @param size_increment Size increment for each subsequent test.
 */

void RunSortingBenchmarks(int num_runs, int initial_size, int size_increment) {
    Instrumentor::Get().BeginSession("Sorting Benchmarks", "results_sorting.json");

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
    SaveProfilingData("results_sorting.json");
}

void RunSearchingBenchmarks(int num_runs, int initial_size, int size_increment) {
    Instrumentor::Get().BeginSession("Searching Benchmarks", "results_searching.json");

    for (int size = initial_size; size <= initial_size + (num_runs - 1) * size_increment; size += size_increment) {
        std::cout << "Running benchmarks for size: " << size << std::endl;
        for (const std::string& caseType : { "Best", "Average", "Worst" }) {
            std::vector<int> data(size);

            if (caseType == "Best") {
                std::iota(data.begin(), data.end(), 0); // Sorted ascending
            }
            else if (caseType == "Worst") {
                std::iota(data.rbegin(), data.rend(), 0); // Sorted descending
            }
            else {
                std::random_device rd;
                std::mt19937 gen(rd());
                std::uniform_int_distribution<> distrib(0, size * 2);
                std::generate(data.begin(), data.end(), [&]() { return distrib(gen); });
                std::sort(data.begin(), data.end()); // Ensure data is sorted
            }

            {
                // Benchmark Binary Search
                std::string name = "Binary Search (" + caseType + ", Size: " + std::to_string(size) + ")";
                InstrumentationTimer timer(name.c_str(), caseType.c_str());
                searching::binary_search(data.data(), data.size(), data[size / 2]);
            }

            {
                // Benchmark Interpolation Search
                std::string name = "Interpolation Search (" + caseType + ", Size: " + std::to_string(size) + ")";
                InstrumentationTimer timer(name.c_str(), caseType.c_str());
                searching::interpolation_once_binary_search(data.data(), data.size(), data[size / 2]);
            }
        }
    }

    Instrumentor::Get().EndSession();
}

void RunVisualizer(std::string filePath) {
    constexpr int screenWidth = 1280;
    constexpr int screenHeight = 900;

    InitWindow(screenWidth, screenHeight, "Sorting Algorithm Visualizer");

    std::vector<TraceEvent> traceEvents = parseJSON(filePath);

    SetTargetFPS(60);

    while (!WindowShouldClose()) {
        BeginDrawing();

        ClearBackground(RAYWHITE);
        DrawText("Sorting Algorithm Visualizer", 10, 10, 20, BLACK);

        if (!traceEvents.empty()) {
            plotData(traceEvents, screenWidth, screenHeight, filePath);
        }
        else {
            DrawText("No data to display.", screenWidth / 2 - 50, screenHeight / 2, 20, RED);
        }

        EndDrawing();
    }

    CloseWindow();
}

bool BENCHMARK = true;
bool VISUALIZE = true;

int main() {

	std::string filePath = "results_searching.json";
    // 	std::string filePath = "results_sorting.json";


    if (BENCHMARK) {
		if (filePath == "results_sorting.json") {
			std::cout << "Running sorting benchmarks..." << std::endl;
			RunSortingBenchmarks(100, 100, 100);
		}
        else {
            std::cout << "Running searching benchmarks..." << std::endl;
            RunSearchingBenchmarks(100, 1000, 1000);
        }
	    
    }

	if (VISUALIZE) {
		RunVisualizer(filePath);
	}

	return 0;
}