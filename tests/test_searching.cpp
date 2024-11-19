#include "sorting.h"
#include <cassert>

void test_merge_sort(){
    std::vector<int> data = {3,2,6,21,3,6};

    sorting::merge_sort(data);

    std::vector<int> expected = {2,3,3,6,6,21};

    assert(data == expected);
}

int main() {
    test_merge_sort();
    return 0;
}