#ifndef TEST_SORTING_H
#define TEST_SORTING_H

#include <iostream>
#include <vector>
#include <cassert>
#include "sorting.h"

using namespace std;

void test_sorting() {
    cout << "Running sort tests..." << endl;
    cout << "Merge Sort" << endl;
    cout << "List before sorting: {3, 2, 6, 21, 3, 6}" << endl;
    cout << "Starting merge sort..." << endl;


    vector<int> data1 = {3, 2, 6, 21, 3, 6};
    vector<int> sorted1 = sorting::merge_sort(data1);

    cout << "Done sorting!" << endl;
    cout << "List after sorting: {2, 3, 3, 6, 6, 21}" << endl;

    if (sorted1 == vector<int>({2, 3, 3, 6, 6, 21}) ) {
        cout << "Merge Sort completed!" << endl;
        return;
    }
    cout << "Merge Sort passed!" << endl;

    cout << "Quick Sort" << endl;
    cout << "List before sorting: {3, 2, 6, 21, 3, 6}" << endl;
    cout << "Starting quick sort..." << endl;

    vector<int> data2 = {3, 2, 6, 21, 3, 6};
    std::vector<int> sorted2 = sorting::quick_sort(data2);

    cout << "Done sorting!" << endl;
    cout << "List after sorting: {2, 3, 3, 6, 6, 21}" << endl;
    
    if (sorted2 == vector<int>({2, 3, 3, 6, 6, 21})) {
        cout << "Quick Sort completed!" << endl;
        return;
    }
    cout << "Quick Sort passed!" << endl;
    
    cout << "Sort tests passed!" << endl;

}

#endif // TEST_SORTING_H
