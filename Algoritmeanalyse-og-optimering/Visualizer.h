#pragma once

#ifndef VISUALIZERAPP_H
#define VISUALIZERAPP_H

#include "json.hpp"
#include "raylib.h"

using json = nlohmann::json;

struct TraceEvent {
    std::string category;
    std::string name;
    int duration;
    std::string phase;
    int processId;
    int threadId;
    long long timestamp;
};

std::vector<TraceEvent> parseJSON(const std::string& filePath);
void plotData(const std::vector<TraceEvent>& data, int screenWidth, int screenHeight, std::string filePath);


#endif // VISUALIZERAPP_H
