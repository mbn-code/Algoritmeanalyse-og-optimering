#ifndef SEARCHING_H
#define SEARCHING_H

#include <iostream>
#include <vector>

/**
 * Binary Search Algorithm Explanation
 * 
 * Binary search is an efficient algorithm for finding a target value in a sorted array.
 * It works by repeatedly dividing the search interval in half:
 * 
 * 1. Start with the entire array
 * 2. Find the middle element
 * 3. If middle element is the target, return its index
 * 4. If target is less than middle, search left half
 * 5. If target is greater than middle, search right half
 * 6. Repeat steps 2-5 until target is found or determined to not exist
 * 
 * Time Complexity: O(log n) - since the search space is halved each time
 * Space Complexity: O(1) for iterative, O(log n) for recursive due to call stack
 * 
 * Requirements:
 * - Array/vector must be sorted in ascending order
 * - Random access to elements is needed
 */


// Iterative Binary Search
namespace searching {
    int binary_search_iter(const std::vector<int>& input, int target) {
    
        std::cout << "Searching for target: " << target << std::endl;
        
        if (input.size()) {
            std::cout << "Currently too big to display full initial array" << std::endl;
            std::cout << "Current 50 first index element values: " << std::endl;
            for (int num : input ) {
                std::cout << num << " ";
                if (num > 50) {
                    break;
                }
            }
            std::cout << std::endl;
        } else {
            std::cout << "Initial array: ";
            for (int num : input) {
                std::cout << num << " ";
            }
            std::cout << std::endl;
        }

        // index for left boundary
        int left = 0;
        // index for right boundary
        int right = input.size() - 1;


        while (left <= right) {
            // middle index of the array / vector
            // This formula avoids integer overflow compared to (left + right) / 2
            // If left and right are large numbers, their sum could exceed the maximum integer value
            // By using this formula, we first calculate the difference (right - left) which is smaller,
            // then divide by 2 and add to left, preventing potential overflow
            int middle_idx = left + (right - left) / 2;
            
            std::cout << "Current boundaries - Left: " << left << ", Middle: " << middle_idx << ", Right: " << right << std::endl;
            std::cout << "Middle index: " << middle_idx << ", Value: " << input[middle_idx] << std::endl;

            if (input[middle_idx] == target) {
                std::cout << "Target found!\n";
                std::cout << "Target " << target << " found at index: " << middle_idx << std::endl;
                return middle_idx;

            } else if (target < input[middle_idx]) {
                std::cout << "Target is less than middle value, updating right boundary\n";
                // update the right boundary (because we're searching for 3 which is lower than 8)
                right = middle_idx - 1;
                std::cout << "New right boundary: " << right << std::endl;
            } else {
                std::cout << "Target is greater than middle value, updating left boundary\n";
                // we virtually move the left boundary to the middle + 1 so we don't get the last middle in the mix.
                left = middle_idx + 1;
            }
        }
        std::cout << "Target " << target << " wasn't found in the dataset";
        
        return -1;
    }

    // Recursive Binary Search
    int binary_search_recur(const std::vector<int>& data, int target, int left, int right) {
        if (left <= right) {
            int middle_idx = left + (right - left) / 2;
            if (data[middle_idx] == target) {
                return middle_idx;
            } else if (target < data[middle_idx]) {
                return binary_search_recur(data, target, left, middle_idx - 1);
            } else {
                return binary_search_recur(data, target, middle_idx + 1, right);
            }
        }
        return -1;
    }
}

#endif // SEARCHING_H
