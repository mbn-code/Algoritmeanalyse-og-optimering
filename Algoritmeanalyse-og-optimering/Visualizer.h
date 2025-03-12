#pragma once

#ifndef VISUALIZERAPP_H
#define VISUALIZERAPP_H

#include "json.hpp"
#include "raylib/raylib-5.5_win64_msvc16/include/raylib.h"

using json = nlohmann::json;

struct TraceEvent {
    std::string category;
    std::string name;
    std::string phase;
    int duration = 0;
    int processId = 0;
    int threadId = 0;
    long long timestamp = 0;

    TraceEvent() = default;
};

std::vector<TraceEvent> parseJSON(const std::string& filePath);
void plotData(const std::vector<TraceEvent>& data, int screenWidth, int screenHeight, std::string filePath);

#endif // VISUALIZERAPP_H
