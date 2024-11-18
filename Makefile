# Compiler and flags
CXX = g++
CXXFLAGS = -Iinclude -Wall -Wextra -std=c++17

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

# Detect OS
ifeq ($(OS),Windows_NT)
    RM = del /Q
    MKDIR = if not exist $(OUT_DIR) mkdir $(OUT_DIR)
    EXE_EXT = .exe
else
    RM = rm -rf
    MKDIR = mkdir -p $(OUT_DIR)
    EXE_EXT =
endif

# Default target
all: $(TARGET)$(EXE_EXT)

# Build the main executable
$(TARGET)$(EXE_EXT): $(OBJS)
    $(MKDIR)
    $(CXX) $(OBJS) -o $(TARGET)$(EXE_EXT)

# Compile object files for the main program
$(OUT_DIR)/%.o: $(SRC_DIR)/%.cpp
    $(MKDIR)
    $(CXX) $(CXXFLAGS) -c $< -o $@

# Build and run tests
tests: $(TEST_OBJS) $(OBJS)
    $(MKDIR)
    $(CXX) $(TEST_OBJS) $(OBJS) -o $(OUT_DIR)/tests$(EXE_EXT)
    @echo "Running tests..."
    @./$(OUT_DIR)/tests$(EXE_EXT)

# Compile object files for tests
$(OUT_DIR)/%.o: $(TEST_DIR)/%.cpp
    $(MKDIR)
    $(CXX) $(CXXFLAGS) -c $< -o $@

# Clean up build artifacts
clean:
    $(RM) $(OUT_DIR)/*.o $(TARGET)$(EXE_EXT) $(OUT_DIR)/tests$(EXE_EXT)

# Phony targets
.PHONY: all clean tests