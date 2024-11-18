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

int main() {
    App app;
    app.run();
    
    return 0;
}