#include <string>
#include <vector>
#include <cmath>
#include <fstream>
#include <iostream>

#include "raylib/raylib-5.5_win64_msvc16/include/raylib.h"
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
			<< ", Timestamp: " << event.timestamp << std::endl; // Timestamp is the specific time the event occurred
    }

    return events;
}

void plotData(const std::vector<TraceEvent>& data, int screenWidth, int screenHeight, std::string filePath) {
    // Prepare for plotting
    const int margin = 60;
    const int plotWidth = screenWidth - 2 * margin;
    const int plotHeight = screenHeight - 2 * margin - 50;

    // Find max duration for scaling
    int maxDuration = 0;
    for (const auto& event : data) {
        if (event.duration > maxDuration) maxDuration = event.duration;
    }

    // Draw plot area background
    DrawRectangle(margin - 10, margin - 10, plotWidth + 20, plotHeight + 20, 
                 Fade(LIGHTGRAY, 0.1f));
    DrawRectangleLines(margin - 10, margin - 10, plotWidth + 20, plotHeight + 20, 
                      Fade(GRAY, 0.2f));

    // Draw background grid with improved aesthetics
    for (int i = 0; i <= 10; i++) {
        int y = margin + (i * plotHeight / 10);
        DrawLine(margin, y, screenWidth - margin, y, 
                Fade(LIGHTGRAY, i % 2 == 0 ? 0.5f : 0.3f));
        
        // Draw Y-axis labels with values
        DrawText(TextFormat("%d μs", (maxDuration * (10 - i) / 10)),
                margin - 50, y - 10, 16, Fade(GRAY, 0.8f));

        int x = margin + (i * plotWidth / 10);
        DrawLine(x, margin, x, screenHeight - margin, 
                Fade(LIGHTGRAY, i % 2 == 0 ? 0.5f : 0.3f));
        
        // Draw X-axis labels
        DrawText(TextFormat("%d", (data.size() * i / 10)),
                x - 20, screenHeight - margin + 10, 16, Fade(GRAY, 0.8f));
    }

    // Draw axes with thicker lines
    DrawLineEx({(float)margin, (float)(screenHeight - margin)}, 
              {(float)(screenWidth - margin), (float)(screenHeight - margin)}, 
              2.0f, BLACK); // X-axis
    DrawLineEx({(float)margin, (float)(screenHeight - margin)}, 
              {(float)margin, (float)margin}, 
              2.0f, BLACK); // Y-axis

    // Draw axis labels with improved styling
    DrawTextPro(GetFontDefault(), "Duration (μs)", 
                {static_cast<float>(margin - 45), 
                 static_cast<float>(margin + plotHeight/2.0f)},
                {0, 0}, 90.0f, 20, 1, DARKGRAY);
    DrawText("Input Size", screenWidth/2 - 40, screenHeight - margin/2, 20, DARKGRAY);

    const float pointSpacing = static_cast<float>(plotWidth) / (data.size() + 1);

    // Draw title and legend with modern styling
    const int legendX = margin + 20;
    const int legendY = margin + 20;
    const int legendSpacing = 30;
    const int legendWidth = 200;
    const int legendHeight = 100;

    // Draw semi-transparent legend background with rounded corners
    Rectangle legendRect = {
        static_cast<float>(legendX - 10),
        static_cast<float>(legendY - 10),
        static_cast<float>(legendWidth),
        static_cast<float>(legendHeight)
    };
    DrawRectangleRounded(legendRect, 0.2f, 10, Fade(WHITE, 0.9f));
    DrawRectangleRounded(legendRect, 0.2f, 10, Fade(GRAY, 0.2f));

    // Draw legend entries based on the file path
    if (filePath == "results_searching.json") {
        DrawText("● Binary Search", legendX, legendY, 20, BLUE);
        DrawText("● Interpolation Search", legendX, legendY + legendSpacing, 20, RED);
        DrawText("O(1)", legendX, legendY + legendSpacing * 2, 16, DARKGRAY);
        DrawText("O(log n)", legendX + 80, legendY + legendSpacing * 2, 16, DARKGREEN);
    } else {
        DrawText("● Merge Sort", legendX, legendY, 20, BLUE);
        DrawText("● Quick Sort", legendX, legendY + legendSpacing, 20, RED);
        DrawText("O(n log n)", legendX, legendY + legendSpacing * 2, 16, DARKBROWN);
        DrawText("O(n²)", legendX + 100, legendY + legendSpacing * 2, 16, MAROON);
    }

    // Plot data points with enhanced visualization
    const float pointRadius = 5.0f;
    Vector2 prevPoint = {0, 0};
    static float animationProgress = 0.0f;
    animationProgress = fmin(animationProgress + 0.02f, 1.0f);
    
    int pointsToDraw = (int)(data.size() * animationProgress);
    
    for (int i = 0; i < pointsToDraw; ++i) {
        float x = margin + (i + 1) * pointSpacing;
        float y = static_cast<float>(screenHeight - margin) - 
                 (static_cast<float>(data[i].duration * plotHeight) / maxDuration);
        Color pointColor = data[i].name.find("Merge") != std::string::npos ? BLUE : RED;

        // Draw connecting lines with gradient effect
        if (i > 0) {
            DrawLineEx(prevPoint, {x, y}, 2.0f, Fade(pointColor, 0.3f));
        }
        
        // Draw points with modern effects
        DrawCircleGradient(static_cast<int>(x), static_cast<int>(y), 
                          pointRadius + 3, Fade(WHITE, 0.8f), Fade(WHITE, 0.1f));
        DrawCircle(static_cast<int>(x), static_cast<int>(y), pointRadius, pointColor);

        // Enhanced tooltip on hover
        Vector2 mousePos = GetMousePosition();
        if (CheckCollisionPointCircle(mousePos, {x, y}, pointRadius + 5)) {
            // Draw tooltip background with shadow effect
            Rectangle tooltipRect = {
                mousePos.x + 10,
                mousePos.y - 50,
                220,
                50
            };
            DrawRectangleRec({mousePos.x + 12, mousePos.y - 52, 220, 50}, 
                            Fade(BLACK, 0.1f)); // Shadow
            DrawRectangleRounded(tooltipRect, 0.2f, 10, WHITE);
            DrawRectangleRounded(tooltipRect, 0.2f, 10, Fade(GRAY, 0.2f));

            // Draw tooltip content
            DrawText(TextFormat("%s", data[i].name.c_str()),
                    static_cast<int>(mousePos.x + 20), 
                    static_cast<int>(mousePos.y - 45), 12, BLACK);
            DrawText(TextFormat("Duration: %d μs", data[i].duration),
                    static_cast<int>(mousePos.x + 20), 
                    static_cast<int>(mousePos.y - 25), 12, DARKGRAY);
        }
        
        prevPoint = {x, y};
    }
}
