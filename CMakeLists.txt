cmake_minimum_required(VERSION 3.15)

# Set the project name and version
project(MyProject VERSION 1.0.0)

# Specify the C++ standard
set(CMAKE_CXX_STANDARD 17)
set(CMAKE_CXX_STANDARD_REQUIRED True)

# Include directories
include_directories(include)

# Add the source files
set(SOURCES
    src/main.cpp
    src/searching.cpp
    src/sorting.cpp
    src/app/App.cpp
)

# Add the header files
set(HEADERS
    src/main.h
    src/app/App.h
    include/searching.h
    include/sorting.h
)

# Add the executable
add_executable(MyProject ${SOURCES} ${HEADERS})

# Add the examples
add_executable(example_struct examples/struct/example.c)
add_executable(algorithm_optimization examples/struct/algorithm_optimization.cpp)

# Add the tests
add_executable(test_searching tests/test_searching.cpp)
add_executable(test_sorting tests/test_sorting.cpp)

# Enable testing
enable_testing()

# Add tests
add_test(NAME TestSearching COMMAND test_searching)
add_test(NAME TestSorting COMMAND test_sorting)

# Platform-specific settings
if(WIN32)
    # Windows-specific settings
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} /W4")
elseif(APPLE)
    # macOS-specific settings
    set(CMAKE_CXX_FLAGS "${CMAKE_CXX_FLAGS} -Wall -Wextra -Wpedantic")
    set(CMAKE_OSX_ARCHITECTURES "arm64")
endif()