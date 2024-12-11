#include "sorting.h"
#include <algorithm>
#include <random>

namespace sorting {

	// Merge Sort implementation
	void merge(std::vector<int>& arr, int left, int mid, int right) {
	    int n1 = mid - left + 1;
	    int n2 = right - mid;

	    std::vector<int> L(n1), R(n2);

	    for (int i = 0; i < n1; ++i)
	        L[i] = arr[left + i];
	    for (int j = 0; j < n2; ++j)
	        R[j] = arr[mid + 1 + j];

	    int i = 0, j = 0, k = left;
	    while (i < n1 && j < n2) {
	        if (L[i] <= R[j]) {
	            arr[k] = L[i];
	            ++i;
	        } else {
	            arr[k] = R[j];
	            ++j;
	        }
	        ++k;
	    }

	    while (i < n1) {
	        arr[k] = L[i];
	        ++i;
	        ++k;
	    }

	    while (j < n2) {
	        arr[k] = R[j];
	        ++j;
	        ++k;
	    }
	}

	void merge_sort(std::vector<int>& arr, int left, int right) {
	    if (left < right) {
	        int mid = left + (right - left) / 2;

	        merge_sort(arr, left, mid);
	        merge_sort(arr, mid + 1, right);

	        merge(arr, left, mid, right);
	    }
	}

	void merge_sort(std::vector<int>& arr) {
	    merge_sort(arr, 0, arr.size() - 1);
	}

	// Quick Sort implementation
	int partition(std::vector<int>& arr, int low, int high, PivotStrategy pivot_strategy) {
	    int pivot_index;
	    switch (pivot_strategy) {
	    case PivotStrategy::FIRST:
	            pivot_index = low;
	            break;
	        case PivotStrategy::LAST:
	            pivot_index = high;
	            break;
	        case PivotStrategy::RANDOM:
	        default:
	            std::random_device rd;
	            std::mt19937 gen(rd());
	            std::uniform_int_distribution<> dis(low, high);
	            pivot_index = dis(gen);
	            break;
	    }
	    std::swap(arr[pivot_index], arr[high]);
	    int pivot = arr[high];
	    int i = (low - 1);

	    for (int j = low; j <= high - 1; ++j) {
	        if (arr[j] < pivot) {
	            ++i;
	            std::swap(arr[i], arr[j]);
	        }
	    }
	    std::swap(arr[i + 1], arr[high]);
	    return (i + 1);
	}

	void quick_sort(std::vector<int>& arr, int low, int high, PivotStrategy pivot_strategy) {
	    if (low < high) {
	        int pi = partition(arr, low, high, pivot_strategy);

	        quick_sort(arr, low, pi - 1, pivot_strategy);
	        quick_sort(arr, pi + 1, high, pivot_strategy);
	    }
	}

} // namespace sorting
