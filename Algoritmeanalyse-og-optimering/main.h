#pragma once

#include <string>
#include <vector>
#include <iostream>
#include <algorithm>
#include <random>
#include <numeric>
#include "raylib/raylib-5.5_win64_msvc16/include/raylib.h"
#include "Instrumentor.h"
#include "sorting.h"
#include "searching.h"
#include "Visualizer.h"

// Progress GUI state structure
struct BenchmarkProgress {
    int currentSize = 0;
    int totalRuns = 0;
    int currentRun = 0;
    std::string currentAlgorithm;
    std::string currentCase;
    float progress = 0.0f;
    std::vector<std::string> recentResults;
    bool isRunning = false;
};

extern BenchmarkProgress gProgress;

void ShowProgressGUI(BenchmarkProgress& progress);
void UpdateProgress(BenchmarkProgress& progress, const std::string& algorithm, 
                   const std::string& caseType, int size, int currentRun, int totalRuns);
void AddResult(BenchmarkProgress& progress, const std::string& result);


void RunSortingBenchmarks(int num_runs, int initial_size, int size_increment);
void RunSearchingBenchmarks(int num_runs, int initial_size, int size_increment);
void RunVisualizer(std::string filePath);
void SaveProfilingData(const std::string& filePath);