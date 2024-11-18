/**
 * @namespace CommandLine
 * @brief Namespace containing functions for command line operations.
 */

/**
 * @brief Runs the command line interface for the application.
 * 
 * This function processes command line arguments and executes the corresponding
 * actions based on the provided options. It supports the following options:
 * - "visualize": Visualizes the process of the algorithms.
 * - "benchmark": Benchmarks the algorithms.
 * 
 * @param argc The number of command line arguments.
 * @param argv The array of command line arguments.
 * 
 * Usage:
 * @code
 * ./app <option>
 * @endcode
 * 
 * Options:
 * - visualize: Visualize the process of the algorithms.
 * - benchmark: Benchmark the algorithms.
 * 
 * If an invalid option is provided, an error message is displayed along with
 * the list of valid options.
 */

#include "App.h"
#include "CommandLine.h"
#include <iostream>

App::App() {/*...*/}
App::~App() {/*...*/}

void App::run() {
    // Implementation of the instance run method
}

void App::run(int argc, char* argv[]) {
    CommandLine::run(argc, argv);
}