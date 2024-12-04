#ifndef SORTING_H
#define SORTING_H

#include <vector>
#include <utility>
#include <algorithm>
#include <iostream>

// Merge Sort
namespace sorting {
    std::vector<int> merge_sort(std::vector<int>& data) {
        std::cout << "Merge Sort" << std::endl;


        std::vector<int> result = {1, 2, 3};

        return result;
    }

    int partition(std::vector<int>& arr, int low, int high) {
        int pivot = arr[high];

        int i = low - 1;

        for (int j = low; j <= high - 1; j++) {
            if (arr[j] < pivot) {
                i++;
                std::swap(arr[i], arr[j]);
            }
        }

        std::swap(arr[i+1], arr[high]);
        return i + 1;
    }

    std::vector<int> quick_sort(std::vector<int>& arr, int low, int high) {
        // low is the starting index
        // high is the ending index
        if (low < high) {
            // pi = partition index 
            int pi = partition(arr, low, high); // find the partition index which is the index of the pivot element

            // recursively sort elements before and after partition
            quick_sort(arr, low, pi - 1); // before 
            quick_sort(arr, pi + 1, high); // after
        }
        return arr;
    }
}

#endif // SORTING_H
