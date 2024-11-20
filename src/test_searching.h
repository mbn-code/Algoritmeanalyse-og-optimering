#ifndef TEST_SEARCHING_H
#define TEST_SEARCHING_H

#include <vector>
#include <cassert>
#include "searching.h"

#include <random> 
#include <algorithm>

std::vector<int> generate_random_dataset(int size, int min_val, int max_val) {
    // Create a random number generator
    std::random_device rd;  // Used to obtain a seed for the random number engine
    std::mt19937 gen(rd()); // Standard mersenne_twister_engine seeded with rd()
    
    // Create a distribution for the specified range
    std::uniform_int_distribution<> dis(min_val, max_val);
    
    // Generate random numbers
    std::vector<int> dataset;
    dataset.reserve(size);
    for(int i = 0; i < size; i++) {
        dataset.push_back(dis(gen));
    }
    
    // Sort the vector since binary search requires sorted data
    std::sort(dataset.begin(), dataset.end());
    
    return dataset;
}


void test_searching() {

    std::vector<int> input = generate_random_dataset(5000, 0, 5000);

    if (searching::binary_search_iter(input, 4) == 2) {
        std::cout << "Binary search iterative test passed!" << std::endl;
    } else {
        std::cout << "Binary search iterative test failed!" << std::endl;
    }

    if (searching::binary_search_recur(input, 4, 0, input.size() - 1) == 2) {
        std::cout << "Binary search recursive test passed!" << std::endl;
    } else {
        std::cout << "Binary search recursive test failed!" << std::endl;
    }
    std::cout << "Search tests completed!" << std::endl;
}

#endif // TEST_SEARCHING_H
