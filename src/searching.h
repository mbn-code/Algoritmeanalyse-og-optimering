#ifndef SEARCHING_H
#define SEARCHING_H

#include <iostream>
#include <vector>

// Iterative Binary Search
namespace searching {
    int binary_search_iter(const std::vector<int>& data, int target) {
        std::cout << "Binary Search Iterative" << std::endl;
        return -1;
    }

    // Recursive Binary Search
    int binary_search_recur(const std::vector<int>& data, int target, int left, int right) {
        std::cout << "Binary Search Recursive" << std::endl;
        return -1;
    }
}

#endif // SEARCHING_H
