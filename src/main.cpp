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
    * @brief Initializes and runs the application.

    Start an instance of the App class and run the application.

    * @details 
    app.run() -> App::run() -> CommandLine::run() -> Benchmark::Run::start() -> Benchmark::Run::Run() -> contains the logic for the benchmarking of the algorithms
    app.run() -> App::run() -> CommandLine::run() -> CommandLine::run() -> contains the logic for the command line options
**/

/* ------------------------------- MAIN_CPP ----------------------------------- */

#include "main.h"
#include "sorting.h"
#include "searching.h"

int main() {

    std::vector<int> data = {1,7,3,4,2,1,7,8,3,6,7,4};
    sorting::merge_sort(data);


    return 0;
}