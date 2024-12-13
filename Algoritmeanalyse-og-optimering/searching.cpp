#include "searching.h"

namespace searching {
    void binary_search(int* arr, int size, int key) {
        int left = 0;
        int right = size - 1;
        while (left <= right) {
            int mid = left + (right - left) / 2;
            if (arr[mid] == key) {
                std::cout << "Element found at index " << mid << std::endl;
                return;
            }
            if (arr[mid] < key) {
                left = mid + 1;
            }
            else {
                right = mid - 1;
            }
        }
        std::cout << "Element not found" << std::endl;
    }
}
