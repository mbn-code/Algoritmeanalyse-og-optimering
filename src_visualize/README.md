# Sorting Algorithm Visualizer

A Python-based interactive visualization tool for understanding sorting algorithms with detailed implementation explanations.

## Features

- **Interactive Visualization**: Real-time visualization of sorting algorithms
- **Multiple Algorithms**: Currently supports:
  - Quick Sort
  - Merge Sort
- **Playback Controls**:
  - Play/Pause
  - Step Forward/Backward
  - Speed Control
  - Progress Slider
- **Educational Elements**:
  - Highlighted Pseudocode
  - Color-coded array elements
  - Operation Counter

## Color Legend

- **Light Blue**: Unsorted elements
- **Yellow**: Pivot element (Quick Sort)
- **Red**: Low/Left index pointer
- **Green**: High/Right index pointer
- **Orange**: Elements being swapped
- **Purple**: Merged elements (Merge Sort)

## Requirements

```bash
pip install matplotlib numpy
```

## Usage

1. Run the program:
```bash
python main.py
```

2. Controls:
   - Use the radio buttons to switch between algorithms
   - Click "Play/Pause" to control animation
   - Use "Step Forward/Backward" for precise control
   - Adjust speed using the speed input box
   - Use the slider to jump to specific points in the sorting process
   - Click "Restart" to begin with a new random array

## Understanding the Display

### Main Components
1. **Visualization Area**: Shows the array as bars
2. **Pseudocode Display**: Shows the current algorithm's code
3. **Control Panel**: Contains all interactive elements
4. **Operation Counter**: Tracks the number of operations

### Algorithm Details

#### Quick Sort
- Uses a pivot-based partitioning approach
- Yellow bar indicates the current pivot
- Red and green bars show the partitioning process

#### Merge Sort
- Divides array into smaller subarrays
- Purple bars show the merging process
- Red and green bars indicate the merge points

## Tips for Educational Use

1. Start with slower speeds to understand each step
2. Use step-by-step mode for detailed analysis
3. Follow the highlighted pseudocode with each operation
4. Observe how different initial arrays affect the sorting process

## Technical Details

- Built using matplotlib for visualization
- Uses generator functions for step-by-step animation
- Implements real-time array manipulation visualization
- Supports dynamic algorithm switching
- Maintains synchronized code highlighting with operations

## Core Components

### 1. PseudoCodeDisplay Class

The `PseudoCodeDisplay` class is responsible for displaying the pseudocode of the current sorting algorithm. It highlights the current line of code being executed.

#### Key Functions:
- `__init__(self, ax)`: Initializes the display with a given matplotlib axis.
- `update(self, line_number)`: Updates the highlighted line of pseudocode.

### 2. SortingAlgorithm Class

The `SortingAlgorithm` class is an abstract base class for all sorting algorithms. It defines the common interface and functionality for the sorting algorithms.

#### Key Functions:
- `__init__(self, array)`: Initializes the sorting algorithm with the given array.
- `sort(self)`: Abstract method to be implemented by subclasses to perform the sorting.

### 3. QuickSort Class

The `QuickSort` class implements the Quick Sort algorithm. It inherits from the `SortingAlgorithm` class.

#### Key Functions:
- `__init__(self, array)`: Initializes the Quick Sort algorithm with the given array.
- `sort(self)`: Performs the Quick Sort algorithm.
- `_partition(self, low, high)`: Partitions the array and returns the pivot index.
- `_quick_sort(self, low, high)`: Recursively sorts the subarrays.

### 4. MergeSort Class

The `MergeSort` class implements the Merge Sort algorithm. It inherits from the `SortingAlgorithm` class.

#### Key Functions:
- `__init__(self, array)`: Initializes the Merge Sort algorithm with the given array.
- `sort(self)`: Performs the Merge Sort algorithm.
- `_merge(self, left, middle, right)`: Merges the subarrays.
- `_merge_sort(self, left, right)`: Recursively sorts the subarrays.

### 5. Visualizer Class

The `Visualizer` class is responsible for managing the visualization of the sorting process. It handles the animation and user interactions.

#### Key Functions:
- `__init__(self, array)`: Initializes the visualizer with the given array.
- `start(self)`: Starts the visualization.
- `pause(self)`: Pauses the visualization.
- `step_forward(self)`: Steps forward in the visualization.
- `step_backward(self)`: Steps backward in the visualization.
- `update_speed(self, speed)`: Updates the speed of the visualization.
- `reset(self)`: Resets the visualization with a new random array.

### Example Code Snippet

```python
import matplotlib.pyplot as plt
import numpy as np

class PseudoCodeDisplay:
    def __init__(self, ax):
        self.ax = ax
        self.lines = []

    def update(self, line_number):
        for i, line in enumerate(self.lines):
            if i == line_number:
                line.set_color('red')
            else:
                line.set_color('black')

class SortingAlgorithm:
    def __init__(self, array):
        self.array = array

    def sort(self):
        raise NotImplementedError

class QuickSort(SortingAlgorithm):
    def __init__(self, array):
        super().__init__(array)

    def sort(self):
        self._quick_sort(0, len(self.array) - 1)

    def _partition(self, low, high):
        pivot = self.array[high]
        i = low - 1
        for j in range(low, high):
            if self.array[j] < pivot:
                i += 1
                self.array[i], self.array[j] = self.array[j], self.array[i]
        self.array[i + 1], self.array[high] = self.array[high], self.array[i + 1]
        return i + 1

    def _quick_sort(self, low, high):
        if low < high:
            pi = self._partition(low, high)
            self._quick_sort(low, pi - 1)
            self._quick_sort(pi + 1, high)

class MergeSort(SortingAlgorithm):
    def __init__(self, array):
        super().__init__(array)

    def sort(self):
        self._merge_sort(0, len(self.array) - 1)

    def _merge(self, left, middle, right):
        n1 = middle - left + 1
        n2 = right - middle
        L = self.array[left:middle + 1]
        R = self.array[middle + 1:right + 1]
        i = j = 0
        k = left
        while i < n1 and j < n2:
            if L[i] <= R[j]:
                self.array[k] = L[i]
                i += 1
            else:
                self.array[k] = R[j]
                j += 1
            k += 1
        while i < n1:
            self.array[k] = L[i]
            i += 1
            k += 1
        while j < n2:
            self.array[k] = R[j]
            j += 1
            k += 1

    def _merge_sort(self, left, right):
        if left < right:
            middle = (left + right) // 2
            self._merge_sort(left, middle)
            self._merge_sort(middle + 1, right)
            self._merge(left, middle, right)

class Visualizer:
    def __init__(self, array):
        self.array = array
        self.fig, self.ax = plt.subplots()
        self.bars = self.ax.bar(range(len(array)), array)
        self.paused = True

    def start(self):
        self.paused = False
        self._animate()

    def pause(self):
        self.paused = True

    def step_forward(self):
        pass  # Implement step forward logic

    def step_backward(self):
        pass  # Implement step backward logic

    def update_speed(self, speed):
        pass  # Implement speed update logic

    def reset(self):
        self.array = np.random.randint(1, 100, len(self.array))
        self._update_bars()

    def _animate(self):
        if not self.paused:
            self._update_bars()
            self.fig.canvas.draw_idle()
            self.fig.canvas.start_event_loop(0.1)

    def _update_bars(self):
        for bar, val in zip(self.bars, self.array):
            bar.set_height(val)

if __name__ == "__main__":
    array = np.random.randint(1, 100, 50)
    visualizer = Visualizer(array)
    visualizer.start()
    plt.show()
```
