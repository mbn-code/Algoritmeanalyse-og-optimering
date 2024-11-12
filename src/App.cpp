#include "App.h"
#include <iostream>

App::App() {
    // Constructor implementation
    // This is run when the object is created
}

App::~App() {
    // Destructor implementation
    // This is run when the object is destroyed
}


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

namespace CommandLine {
    void run(int argc, char* argv[]) {
        if (argc < 2) {
            std::cerr << "Usage: " << argv[0] << " <option>" << std::endl;
            std::cerr << "Options:" << std::endl;
            std::cerr << "  visualize   Visualize the process of the algorithms" << std::endl;
            std::cerr << "  benchmark   Benchmark the algorithms" << std::endl;
            return;
        }

        std::string option = argv[1];
        if (option == "visualize") {
            std::cout << "Visualizing the process of the algorithms..." << std::endl;
            // Call the visualization function here
        } else if (option == "benchmark") {
            std::cout << "Benchmarking the algorithms..." << std::endl;
            // Call the benchmarking function here
        } else {
            std::cerr << "Invalid option: " << option << std::endl;
            std::cerr << "Options:" << std::endl;
            std::cerr << "  visualize   Visualize the process of the algorithms" << std::endl;
            std::cerr << "  benchmark   Benchmark the algorithms" << std::endl;
        }
    }
}

// This is the run method that is called when the object is created //
/*
Use App::run(int argc, char* argv[]) as an entry point, such as in main.cpp, to start the application.

This static run method (the one directly under this comment) internally creates an instance
of App and calls its run() instance method, which then performs the actual work of running the application.
*/
void App::run() {
    // Implementation of the run method
    std::cout << "Running the app, version: " << version << std::endl;
    // This is run when the run method is called on the object from main
}

// static method to run the app without creating an object of the class App //
/*
This is what's called from main.cpp which then calls the run method on the object
*/
void App::run([[maybe_unused]] int argc, [[maybe_unused]] char* argv[]) {
    App app;
    app.run();
    // we call app.run() so that the run method is executed and the message is printed
}