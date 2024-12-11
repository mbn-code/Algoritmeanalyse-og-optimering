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
    * @brief Runs the CLI application

    * @details

**/

/* ------------------------------- MAIN_CPP ----------------------------------- */

#include <iostream>
#include <vector>
#include <string>
#include "searching.h"
#include "sorting.h"
#include "test_searching.h"
#include "test_sorting.h"
#include <filesystem>

namespace fs = std::filesystem;

void CLI() {
    std::string command;
    std::cout << "\n=== Algorithm Testing CLI ===\n";

    while (true) {
        std::cout << "\nAvailable commands:\n";
        std::cout << "1. test_sorting   - Run sorting algorithm tests\n";
        std::cout << "2. test_searching - Run searching algorithm tests\n";
        std::cout << "3. exit           - Exit the program\n\n";

        std::cout << "Enter command: ";
        std::cin >> command;

        if (command == "test_sorting") {
            std::cout << "\nRunning sorting tests...\n";
            test_sorting();
        } else if (command == "test_searching") {
            std::cout << "\nRunning searching tests...\n";
            test_searching();
        } else if (command == "exit") {
            std::cout << "\nExiting program. Goodbye!\n";
            break;
        } else {
            std::cout << "\nError: Unknown command '" << command << "'\n";
            std::cout << "Please use one of the available commands listed above.\n";
        }
    }
}

int main() {

    if (!fs::exists("src_visualize")) {
        fs::create_directory("src_visualize");
    }

    CLI();
    return 0;
}