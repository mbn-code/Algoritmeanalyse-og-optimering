#include "CommandLine.h"
#include <iostream>
#include <string>

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