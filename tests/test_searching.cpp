#include "searching.h"
#include <algorithm>
#include <cassert>

void test_merge_sort(){
    std::vector<int> data = {2, 3, 4, 5, 8};

    int index = searching::binary_search_iter(data,4);
    int index = searching::binary_search_recur(data,4);

    assert(index == 2);

}

int main() {
    test_merge_sort();
    return 0;
}