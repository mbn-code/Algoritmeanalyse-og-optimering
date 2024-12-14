#pragma once

#ifndef MAIN_H

#include "sorting.h"
#include "searching.h"

#include <vector>
#include <algorithm>
#include <numeric>
#include <random>

#include "Instrumentor.h"
#include "raylib.h"
#include "json.hpp"
#include "Visualizer.h"

#include <iostream>
#include <fstream>


void RunSortingBenchmarks(int num_runs, int initial_size, int size_increment);
void RunSearchingBenchmarks(int num_runs, int initial_size, int size_increment);

int main();

#endif // !MAIN_H