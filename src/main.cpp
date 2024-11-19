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

void CLI() {
    std::string command;
    while (true) {
        std::cout << "Enter command (test_sorting, test_searching, or exit): ";
        std::cin >> command;
        if (command == "test_sorting") {
            test_sorting();
        } else if (command == "test_searching") {
            test_searching();
        } else if (command == "exit") {
            break;
        } else {
            std::cout << "Unknown command. Please enter 'test_sorting', 'test_searching', or 'exit'." << std::endl;
        }
    }
}

int main() {
    CLI();
    return 0;
}