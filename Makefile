# Compiler and flags
CXX = g++
CXXFLAGS = -Iinclude -Wall -Wextra -std=c++17
LDFLAGS = -o out/main

# Directories
SRC_DIR = src
INCLUDE_DIR = include
OUT_DIR = out
TEST_DIR = tests

# Source and object files
SRCS = $(wildcard $(SRC_DIR)/*.cpp)
OBJS = $(SRCS:$(SRC_DIR)/%.cpp=$(OUT_DIR)/%.o)
TEST_SRCS = $(wildcard $(TEST_DIR)/*.cpp)
TEST_OBJS = $(TEST_SRCS:$(TEST_DIR)/%.cpp=$(OUT_DIR)/%.o)

# Target executable
TARGET = $(OUT_DIR)/main

# Default target
all: $(TARGET)

# Build the main executable
$(TARGET): $(OBJS)
	@mkdir -p $(OUT_DIR)
	$(CXX) $(OBJS) $(LDFLAGS)

# Compile object files for the main program
$(OUT_DIR)/%.o: $(SRC_DIR)/%.cpp
	@mkdir -p $(OUT_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Build and run tests
tests: $(TEST_OBJS) $(OBJS)
	@mkdir -p $(OUT_DIR)
	$(CXX) $(TEST_OBJS) $(OBJS) -o $(OUT_DIR)/tests
	@echo "Running tests..."
	@./$(OUT_DIR)/tests

# Compile object files for tests
$(OUT_DIR)/%.o: $(TEST_DIR)/%.cpp
	@mkdir -p $(OUT_DIR)
	$(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up build artifacts
clean:
	rm -rf $(OUT_DIR)/*.o $(TARGET) $(OUT_DIR)/tests

# Phony targets
.PHONY: all clean tests
