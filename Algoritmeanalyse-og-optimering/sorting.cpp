#include "sorting.h"
#include <algorithm>
#include <random>

namespace sorting {

    // Merge Sort implementation
    void merge(std::vector<int>& arr, int left, int mid, int right) {
        // Step 1: Calculate sizes of the two subarrays
        int n1 = mid - left + 1;   // O(1)
        int n2 = right - mid;      // O(1)

        // Step 2: Create temporary arrays
        std::vector<int> L(n1), R(n2);  // O(n) for allocation

        // Step 3: Copy data into the left subarray
        for (int i = 0; i < n1; ++i)   // O(n1) or O(n)
            L[i] = arr[left + i];      // O(1)
        
        // Step 4: Copy data into the right subarray
        for (int j = 0; j < n2; ++j)   // O(n2) or O(n)
            R[j] = arr[mid + 1 + j];   // O(1)

        // Step 5: Merge the two subarrays
        int i = 0, j = 0, k = left;    // O(1)
        
        while (i < n1 && j < n2) {      // O(n) - comparing and merging
            if (L[i] <= R[j]) {         // O(1)
                arr[k] = L[i];          // O(1)
                ++i;                    // O(1)
            } else {
                arr[k] = R[j];          // O(1)
                ++j;                    // O(1)
            }
            ++k;                        // O(1)
        }

        // Step 6: Copy remaining elements from L, if any
        while (i < n1) {                // O(n1)
            arr[k] = L[i];              // O(1)
            ++i;                        // O(1)
            ++k;                        // O(1)
        }

        // Step 7: Copy remaining elements from R, if any
        while (j < n2) {                // O(n2)
            arr[k] = R[j];              // O(1)
            ++j;                        // O(1)
            ++k;                        // O(1)
        }
    }

    void merge_sort(std::vector<int>& arr, int left, int right) {
        if (left < right) {                  // O(1) - base case check
            // Step 1: Calculate middle index
            int mid = left + (right - left) / 2;  // O(1)

            // Step 2: Recursively sort the left half
            merge_sort(arr, left, mid);          // O(log n) - recursive call

            // Step 3: Recursively sort the right half
            merge_sort(arr, mid + 1, right);     // O(log n) - recursive call

            // Step 4: Merge the two sorted halves
            merge(arr, left, mid, right);         // O(n)
        }
    }

    // This is a wrapper function for simplicity
    void merge_sort(std::vector<int>& arr) {
        merge_sort(arr, 0, arr.size() - 1);  // O(log n) recursive calls
    }

    // Quick Sort implementation
    int partition(std::vector<int>& arr, int low, int high, PivotStrategy pivot_strategy) {
        // Step 1: Choose pivot based on strategy (First, Last, or Random)
        int pivot_index;
        switch (pivot_strategy) {
            case PivotStrategy::FIRST:            // O(1)
                pivot_index = low;               // O(1)
                break;
            case PivotStrategy::LAST:             // O(1)
                pivot_index = high;              // O(1)
                break;
            case PivotStrategy::RANDOM:           // O(1)
            default:                             // O(1)
                std::random_device rd;           // O(1)
                std::mt19937 gen(rd());          // O(1)
                std::uniform_int_distribution<> dis(low, high); // O(1)
                pivot_index = dis(gen);          // O(1)
                break;
        }

        // Step 2: Swap pivot with last element
        std::swap(arr[pivot_index], arr[high]);  // O(1)

        // Step 3: Initialize pivot and `i`
        int pivot = arr[high];                 // O(1)
        int i = low - 1;                      // O(1)

        // Step 4: Loop through the array to partition
        for (int j = low; j <= high - 1; ++j) {    // O(n)
            if (arr[j] < pivot) {                   // O(1)
                ++i;                                // O(1)
                std::swap(arr[i], arr[j]);          // O(1)
            }
        }

        // Step 5: Swap pivot into its correct position
        std::swap(arr[i + 1], arr[high]);      // O(1)
        return (i + 1);                        // O(1)
    }

    void quick_sort(std::vector<int>& arr, int low, int high, PivotStrategy pivot_strategy) {
        if (low < high) {                           // O(1) - base case check
            // Step 1: Partition the array
            int pi = partition(arr, low, high, pivot_strategy);   // O(n)

            // Step 2: Recursively sort the left part
            quick_sort(arr, low, pi - 1, pivot_strategy);          // O(log n)

            // Step 3: Recursively sort the right part
            quick_sort(arr, pi + 1, high, pivot_strategy);         // O(log n)
        }
    }

} // namespace sorting
