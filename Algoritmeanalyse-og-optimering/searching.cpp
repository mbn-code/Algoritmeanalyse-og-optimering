#include "searching.h"

namespace searching {
    void binary_search(int* arr, int size, int key) {
        int left = 0;                      // O(1)
        int right = size - 1;              // O(1)
        while (left <= right) {            // O(log n) - loop runs log(n) times
            int mid = left + (right - left) / 2;  // O(1)
            if (arr[mid] == key) {         // O(1)
                std::cout << "Element found at index " << mid << std::endl;  // O(1)
                return;                    // O(1)
            }
            if (arr[mid] < key) {          // O(1)
                left = mid + 1;            // O(1)
            }
            else {                         // O(1)
                right = mid - 1;           // O(1)
            }
        }
        std::cout << "Element not found" << std::endl;  // O(1)
    }

    // Implementation of Interpolation Search
    int interpolation_once_binary_search(const int* arr, int size, int target) {
        int low = 0, high = size - 1;

        while (low <= high && target >= arr[low] && target <= arr[high]) {
            if (low == high) {
                if (arr[low] == target) return low;
                return -1;
            }

            // Probing position
            int pos = low + ((target - arr[low]) * (high - low)) / (arr[high] - arr[low]);

            // If found at pos
            if (arr[pos] == target)
                return pos;

            // Target is in upper part
            if (arr[pos] < target)
                low = pos + 1;
            // Target is in lower part
            else
                high = pos - 1;
        }

        return -1; // Element not found
    }
}