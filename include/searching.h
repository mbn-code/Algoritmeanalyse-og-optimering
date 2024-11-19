#ifndef SEARCHING_H
#define SEARCHING_H

#include <vector>

namespace searching {
    int binary_search_iter(std::vector<int>& data, int target);
    int binary_search_recur(std::vector<int>& data, int target);
}


#endif // SEARCHING_H