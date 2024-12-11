#ifndef SORTING_H
#define SORTING_H

#include <vector>

namespace sorting {
    // Function to perform merge sort on a vector of integers
    void merge_sort(std::vector<int>& data);

    // Enum for pivot selection strategy
    enum class PivotStrategy {
        RANDOM,
        LAST
    };

    // Function to set pivot strategy
    void set_pivot_strategy(PivotStrategy strategy);

    // Function to perform quick sort on a vector of integers
    void quick_sort(std::vector<int>& arr, int low, int high);

    // Function to perform quick sort with middle pivot on a vector of integers
    void quick_sort_middle(std::vector<int>& arr, int low, int high);
}

#endif // SORTING_H
