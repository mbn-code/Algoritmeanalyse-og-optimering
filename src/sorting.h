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


    int partition(std::vector<int>& arr, int low, int high) {
        // Select pivot index randomly
        int pivotIdx = low + rand() % (high - low + 1);
        // Get actual pivot value
        int pivotValue = arr[pivotIdx];
        // Move pivot to end
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
