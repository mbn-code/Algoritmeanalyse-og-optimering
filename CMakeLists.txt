cmake_minimum_required(VERSION 3.10)

project(Algoritmeanalyse)

set(CMAKE_CXX_STANDARD 17)

# Add source files
add_executable(AlgorithmProject
        src/main.cpp
    src/searching.h
    src/sorting.h
    src/test_searching.h
    src/test_sorting.h
)

# If you want to run tests separately, you can add a test target
# enable_testing()
# add_test(NAME test_sorting COMMAND ./AlgorithmProject test_sorting)
