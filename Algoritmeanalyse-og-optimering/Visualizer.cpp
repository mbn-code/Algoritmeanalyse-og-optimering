#include <algorithm>
#include <numeric>
#include <random>
#include <string>
#include <vector>
#include <cmath>
#include <fstream>
#include <iostream>

#include <raylib.h>
#include "Visualizer.h"

using json = nlohmann::json;

std::vector<TraceEvent> parseJSON(const std::string& filePath) {
    std::vector<TraceEvent> events;

    // Read and parse JSON file
    std::ifstream inputFile(filePath);
    if (!inputFile.is_open()) {
        std::cerr << "Error: Could not open " << filePath << std::endl;
        return events;
    }

    json jsonData;
    inputFile >> jsonData;

    for (const auto& event : jsonData["traceEvents"]) {
        TraceEvent trace;
        trace.category = event["cat"].get<std::string>();
        trace.name = event["name"].get<std::string>();
        trace.duration = event["dur"].get<int>();
        trace.phase = event["ph"].get<std::string>();
        trace.processId = event["pid"].get<int>();
        trace.threadId = event["tid"].get<int>();
        trace.timestamp = event["ts"].get<long long>();
        events.push_back(trace);
    }

    // Debug output
    for (const auto& event : events) {
        std::cout << "Category: " << event.category << ", Name: " << event.name
            << ", Duration: " << event.duration << ", Phase: " << event.phase
            << ", PID: " << event.processId << ", TID: " << event.threadId
            << ", Timestamp: " << event.timestamp << std::endl;
    }

    return events;
}

void plotData(const std::vector<TraceEvent>& data, int screenWidth, int screenHeight, std::string filePath) {
    // Prepare for plotting
    int margin = 50;
    int plotWidth = screenWidth - 2 * margin;
    int plotHeight = screenHeight - 2 * margin;

    // Find max duration for scaling
    int maxDuration = 0;
    for (const auto& event : data) {
        if (event.duration > maxDuration) maxDuration = event.duration;
    }

    // Draw axes
    DrawLine(margin, screenHeight - margin, screenWidth - margin, screenHeight - margin, BLACK); // X-axis
    DrawLine(margin, screenHeight - margin, margin, margin, BLACK);                              // Y-axis



    // Adjust point spacing based on the file type
    int pointSpacing;
    if (filePath == "results_searching.json") {
        pointSpacing = plotWidth / (data.size() + 1)*1.5; // Use a smaller point spacing for searching
        DrawText("Binary Search", margin + 10, margin + 10, 20, BLACK);
        DrawText("O(1)", margin + 10, screenHeight - margin - 10, 10, DARKGRAY);
        DrawText("O(log n)", margin + 10, screenHeight - margin - 30, 10, DARKGREEN);
    }
    else if (filePath == "results_sorting.json") {
        pointSpacing = plotWidth / (data.size() + 1) * 2; // Use a larger point spacing for sorting
        DrawText("Merge Sort", margin + 10, margin + 10, 20, BLACK);
        DrawText("Quick Sort", margin + 10, margin + 30, 20, BLACK);
        DrawText("O(n log n)", margin + 10, screenHeight - margin - 10, 10, DARKBROWN);
        DrawText("O(n^2)", margin + 10, screenHeight - margin - 30, 10, ORANGE);
    }

    // Plot data points and connect them
    int pointRadius = 2;
    // Dynamically color points based on input size or some attribute
    for (size_t i = 0; i < data.size(); ++i) {
        int x = margin + (i + 1) * pointSpacing;
        int y = screenHeight - margin - (data[i].duration * plotHeight / maxDuration);

        // Dynamically color points based on more granular categories
        Color pointColor = BLUE;  // Default color

        if (data[i].duration < 10) {
            pointColor = GRAY;  // Extremely fast operations
        }
        else if (data[i].duration < 25) {
            pointColor = GREEN;  // Very fast operations (small input size)
        }
        else if (data[i].duration < 50) {
            pointColor = DARKGREEN;  // Fast operations
        }
        else if (data[i].duration < 100) {
            pointColor = DARKBLUE;  // Slightly slower but still fast
        }
        else if (data[i].duration < 150) {
            pointColor = ORANGE;  // Moderate speed, a bit slower
        }
        else if (data[i].duration < 200) {
            pointColor = ORANGE;  // Moderate speed
        }
        else if (data[i].duration < 300) {
            pointColor = GOLD;  // Slower operations
        }
        else if (data[i].duration < 400) {
            pointColor = ORANGE;  // Noticeably slow operations
        }
        else if (data[i].duration < 500) {
            pointColor = RED;  // Quite slow operations
        }
        else if (data[i].duration < 600) {
            pointColor = RED;  // Very slow operations
        }
        else if (data[i].duration < 800) {
            pointColor = MAROON;  // Extremely slow operations
        }
        else if (data[i].duration < 1000) {
            pointColor = BROWN;  // Unusually slow
        }
        else if (data[i].duration < 1500) {
            pointColor = PURPLE;  // Very long-running operations
        }
        else if (data[i].duration < 2000) {
            pointColor = DARKPURPLE;  // Borderline inefficient
        }
        else if (data[i].duration < 3000) {
            pointColor = BROWN;  // Terrible performance
        }
        else if (data[i].duration < 4000) {
            pointColor = DARKBROWN;  // Extremely inefficient
        }
        else {
            pointColor = BLACK;  // Unreasonably slow (outlier)
        }


        // Draw the point at calculated position with the chosen color
        DrawCircle(x, y, pointRadius, pointColor);
    }

    // Plot theoretical asymptotes
    auto plotAsymptote = [&](auto func, Color color) {
        for (int i = 0; i < plotWidth; ++i) {
            int x = margin + i;
            int y = screenHeight - margin - (func(i) * plotHeight / maxDuration);
            if (y < margin) y = margin;
            DrawPixel(x, y, color);
        }
        };

    plotAsymptote([](int n) { return 1; }, DARKGRAY); // O(1)
    plotAsymptote([](int n) { return std::log(n); }, DARKGREEN); // O(log n)
    plotAsymptote([](int n) { return std::log(std::log(n)); }, DARKBLUE); // O(log log n)
    plotAsymptote([](int n) { return n; }, DARKPURPLE); // O(n)
    plotAsymptote([](int n) { return n * std::log(n); }, DARKBROWN); // O(n log n)
    plotAsymptote([](int n) { return n * n; }, ORANGE); // O(n^2)
    plotAsymptote([](int n) { return std::exp(n); }, RED); // O(e^n)
    plotAsymptote([](int n) { return std::tgamma(n + 1); }, PURPLE); // O(n!)
}
