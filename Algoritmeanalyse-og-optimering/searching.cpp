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
		int left = 0, right = size - 1;                                                         // O(1)

		while (left <= right && target >= arr[left] && target <= arr[right]) {                  // O(log n)
			if (left == right) {                                                                // O(1)
				if (arr[left] == target) return left;                                           // O(1) 
                return -1;
            }

            // Probing position
			int pos = left + ((target - arr[left]) * (right - left)) / (arr[right] - arr[left]); // O(1)

            // If found at pos
			if (arr[pos] == target)                                                             // O(1)
				return pos;                                                                     // O(1)

            // Target is in upper part 
			if (arr[pos] < target)                                                              // O(1)
				left = pos + 1;                                                                 // O(1)
            // Target is in lefter part
            else
				right = pos - 1;                                                                // O(1)
        }

        return -1; // Element not found
    }
}