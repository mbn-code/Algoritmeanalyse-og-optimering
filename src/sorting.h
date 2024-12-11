#ifndef SORTING_H
#define SORTING_H

#include <vector>
#include <utility>
#include <algorithm>
#include <iostream>

// Merge Sort
namespace sorting {
    void merge(std::vector<int>& data, int left, int mid, int right) {
        int n1 = mid - left + 1;
        int n2 = right - mid;
        std::vector<int> L(n1), R(n2);
        int i, j, k;
        for (i = 0; i < n1; ++i)
            L[i] = data[left + i];
        for (j = 0; j < n2; ++j)
            R[j] = data[mid + 1 + j];
        i = 0; j = 0; k = left;
        while (i < n1 && j < n2) {
            if (L[i] <= R[j])
                data[k++] = L[i++];
            else
                data[k++] = R[j++];
        }
        while (i < n1)
            data[k++] = L[i++];
        while (j < n2)
            data[k++] = R[j++];
    }

    void merge_sort_rec(std::vector<int>& data, int left, int right) {
        if (left < right) {
            int mid = left + (right - left) / 2;
            merge_sort_rec(data, left, mid);
            merge_sort_rec(data, mid + 1, right);
            merge(data, left, mid, right);
        }
    }

    void merge_sort(std::vector<int>& data) {
        merge_sort_rec(data, 0, data.size() - 1);
    }

    // Enum for pivot selection strategy
    enum class PivotStrategy {
        RANDOM,
        LAST
    };

    // Global variable for pivot strategy
    static PivotStrategy currentPivotStrategy = PivotStrategy::RANDOM;

    // Function to set pivot strategy
    void set_pivot_strategy(PivotStrategy strategy) {
        currentPivotStrategy = strategy;
    }

    int partition(std::vector<int>& arr, int low, int high) {
        int pivotIdx;
        
        // Select pivot based on strategy
        switch (currentPivotStrategy) {
            case PivotStrategy::RANDOM:
                pivotIdx = low + rand() % (high - low + 1);
                break;
            case PivotStrategy::LAST:
                pivotIdx = high;
                break;
        }

        int pivotValue = arr[pivotIdx];
        std::swap(arr[pivotIdx], arr[high]);
        
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] < pivotValue) {
                i++;
                std::swap(arr[i], arr[j]);
            }
        }
        std::swap(arr[i + 1], arr[high]);
        return i + 1;
    }

    void quick_sort(std::vector<int>& arr, int low, int high) {
        if (low < high) {
            int pi = partition(arr, low, high);
            quick_sort(arr, low, pi - 1);
            quick_sort(arr, pi + 1, high);
        }
    }


    int partition_middle(std::vector<int>& arr, int low, int high) {
        int pivotIdx = low + (high - low) / 2; // Middle pivot
        int pivotValue = arr[pivotIdx];
        std::swap(arr[pivotIdx], arr[high]);
        
        int i = low - 1;
        
        for (int j = low; j < high; j++) {
            if (arr[j] < pivotValue) {
                i++;
                std::swap(arr[i], arr[j]);
            }
        }
        std::swap(arr[i + 1], arr[high]);
        return i + 1;
    }

    void quick_sort_middle(std::vector<int>& arr, int low, int high) {
        if (low < high) {
            int pi = partition_middle(arr, low, high);
            quick_sort_middle(arr, low, pi - 1);
            quick_sort_middle(arr, pi + 1, high);
        }
    }
}

#endif // SORTING_H
