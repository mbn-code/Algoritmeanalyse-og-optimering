#ifndef TEST_SEARCHING_H
#define TEST_SEARCHING_H

#include <vector>
#include <cassert>
#include "searching.h"

void test_searching() {
    std::vector<int> data = {2, 3, 4, 5, 8};
    assert(searching::binary_search_iter(data, 4) == 2);
    assert(searching::binary_search_recur(data, 4, 0, data.size() - 1) == 2);
    std::cout << "Search tests passed!" << std::endl;
}

#endif // TEST_SEARCHING_H
