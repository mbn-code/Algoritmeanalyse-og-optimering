#ifndef TEST_SORTING_H
#define TEST_SORTING_H

#include <iostream>
#include <vector>
#include <cassert>
#include "sorting.h"

void test_sorting() {
    std::vector<int> data1 = {3, 2, 6, 21, 3, 6};
    sorting::merge_sort(data1);
    assert(data1 == std::vector<int>({2, 3, 3, 6, 6, 21}));

    std::vector<int> data2 = {3, 2, 6, 21, 3, 6};
    sorting::quick_sort(data2);
    assert(data2 == std::vector<int>({2, 3, 3, 6, 6, 21}));

    std::cout << "Sort tests passed!" << std::endl;

}

#endif // TEST_SORTING_H
