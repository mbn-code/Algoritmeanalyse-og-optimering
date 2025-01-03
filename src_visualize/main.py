import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
from matplotlib.gridspec import GridSpec
import sys
sys.setrecursionlimit(1500)

class PseudoCodeDisplay:
    """Displays pseudocode and highlights the current line during execution."""
    def __init__(self, ax, pseudocode):
        self.ax = ax
        self.code_lines = pseudocode.strip().split('\n')
        self.text_objects = []

        # Display pseudocode lines
        for i, line in enumerate(self.code_lines):
            txt = self.ax.text(
                0.01, 0.95 - i * 0.05, line, fontsize=10,
                transform=self.ax.transAxes, ha='left',
                backgroundcolor='white'
            )
            self.text_objects.append(txt)
        self.ax.axis('off')

    def highlight_line(self, line_number):
        # Reset previous highlights
        for txt in self.text_objects:
            txt.set_backgroundcolor('white')
        # Highlight the current line
        if 0 <= line_number < len(self.text_objects):
            self.text_objects[line_number].set_backgroundcolor('yellow')

    def update_code(self, pseudocode):
        # Clear existing text objects
        for txt in self.text_objects:
            txt.remove()
        self.code_lines = pseudocode.strip().split('\n')
        self.text_objects = []
        # Re-display pseudocode lines
        for i, line in enumerate(self.code_lines):
            txt = self.ax.text(
                0.01, 0.95 - i * 0.05, line, fontsize=10,
                transform=self.ax.transAxes, ha='left',
                backgroundcolor='white'
            )
            self.text_objects.append(txt)
        self.ax.figure.canvas.draw_idle()

class SortVisualizer:
    """Visualizes sorting algorithms with interactive controls and pseudocode."""
    def __init__(self, array):
        self.array = array.copy()
        self.original_array = array.copy()  # Keep the original array for reset
        self.operations = 0
        self.algorithm = "merge"
        self.interval = 0.2  # Default interval in seconds
        self.paused = False
        self.frames = []
        self.precomputed_frames = {}
        self.target_value = array[len(array) // 2]  # Default target value for binary search

        # Set up the figure and axes with improved layout
        self.fig = plt.figure(figsize=(14, 8))
        gs = GridSpec(2, 3, width_ratios=[3, 1, 1], height_ratios=[4, 1])
        self.ax = self.fig.add_subplot(gs[0, 0])
        self.pseudo_ax = self.fig.add_subplot(gs[0, 1])
        self.info_ax = self.fig.add_subplot(gs[0, 2])
        self.control_ax = self.fig.add_subplot(gs[1, :])
        self.control_ax.axis('off')
        plt.subplots_adjust(wspace=0.3, hspace=0.3)

        # Initialize the plot elements
        self.bar_rects = self.ax.bar(range(len(self.array)), self.array, align="edge", color='lightblue')
        self.ax.set_title("Sorting Visualization")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        self.ax.set_xlim(0, len(self.array))
        self.ax.set_ylim(0, int(max(self.array) * 1.1))

        # Display operation count
        self.operation_text = self.info_ax.text(0.5, 0.5, f"Operations: {self.operations}", fontsize=12,
                                                ha='center', va='center', transform=self.info_ax.transAxes)
        self.info_ax.axis('off')

        # Create legend
        legend_patches = [
            mpatches.Patch(color='lightblue', label='Unsorted elements'),
            mpatches.Patch(color='yellow', label='Pivot element'),
            mpatches.Patch(color='red', label='Low/Left index'),
            mpatches.Patch(color='green', label='High/Right index'),
            mpatches.Patch(color='orange', label='Swapped elements'),
            mpatches.Patch(color='purple', label='Merged elements'),
        ]
        self.ax.legend(handles=legend_patches, loc='upper right')

        # Initialize pseudocode display and precompute frames
        self.define_pseudocode()
        self.pseudocode_display = PseudoCodeDisplay(self.pseudo_ax, self.pseudocode)
        self.precompute_frames()

        # Set up GUI controls with additional buttons
        self.setup_gui()

    def define_pseudocode(self):
        """Defines the pseudocode for the selected sorting algorithm with line numbers."""
        if self.algorithm == "merge":
            # Updated pseudocode with line numbers
            self.pseudocode = '''
    1 def merge_sort(arr, left, right):
    2     if left >= right:
    3         return
    4     mid = (left + right) // 2
    5     merge_sort(arr, left, mid)
    6     merge_sort(arr, mid + 1, right)
    7     merge(arr, left, mid, right)

    8 def merge(arr, left, mid, right):
    9     merged = []
    10    i, j = left, mid + 1
    11    while i <= mid and j <= right:
    12        if arr[i] <= arr[j]:
    13            merged.append(arr[i])
    14            i += 1
    15        else:
    16            merged.append(arr[j])
    17            j += 1
    18    while i <= mid:
    19        merged.append(arr[i])
    20        i += 1
    21    while j <= right:
    22        merged.append(arr[j])
    23        j += 1
    24    for k, val in enumerate(merged):
    25        arr[left + k] = val
    '''

        elif self.algorithm == "quick":
            # Updated pseudocode with line numbers
            self.pseudocode = '''
    1 def quick_sort(arr, low, high):
    2     if low < high:
    3         pi = partition(arr, low, high)
    4         quick_sort(arr, low, pi - 1)
    5         quick_sort(arr, pi + 1, high)

    6 def partition(arr, low, high):
    7     pivot = arr[high]
    8     i = low
    9     for j in range(low, high):
    10        if arr[j] < pivot:
    11            arr[i], arr[j] = arr[j], arr[i]
    12            i += 1
    13    arr[i], arr[high] = arr[high], arr[i]
    14    return i
    '''
        elif self.algorithm == "binary":
            self.pseudocode = '''
1 def binary_search(arr, target):
2     left = 0
3     right = len(arr) - 1
4     while left <= right:
5         mid = (left + right) // 2
6         if arr[mid] == target:
7             return mid
8         elif arr[mid] < target:
9             left = mid + 1
10        else:
11            right = mid - 1
12    return -1
'''

    # Updated generator functions with correct line numbers
    def merge_sort_generator(self, arr, left, right):
        """Generator for merge sort algorithm visualization."""
        yield arr.copy(), {}, 1  # Line 1: def merge_sort...
        if left >= right:
            yield arr.copy(), {}, 2  # Line 2: if left >= right...
            yield arr.copy(), {}, 3  # Line 3: return
            return
        mid = (left + right) // 2
        yield arr.copy(), {}, 4  # Line 4: mid = ...
        yield arr.copy(), {}, 5  # Line 5: merge_sort(arr, left, mid)
        yield from self.merge_sort_generator(arr, left, mid)
        yield arr.copy(), {}, 6  # Line 6: merge_sort(arr, mid + 1, right)
        yield from self.merge_sort_generator(arr, mid + 1, right)
        yield arr.copy(), {}, 7  # Line 7: merge(arr, left, mid, right)
        yield from self.merge_generator(arr, left, mid, right)

    def merge_generator(self, arr, left, mid, right):
        """Generator for merging in merge sort."""
        yield arr.copy(), {}, 8   # Line 8: def merge...
        merged = []
        yield arr.copy(), {}, 9   # Line 9: merged = []
        i, j = left, mid + 1
        yield arr.copy(), {}, 10  # Line 10: i, j = ...
        while i <= mid and j <= right:
            yield arr.copy(), {'left': i, 'right': j}, 11  # Line 11: while i <= mid and j <= right
            if arr[i] <= arr[j]:
                yield arr.copy(), {'left': i}, 12  # Line 12: if arr[i] <= arr[j]
                merged.append(arr[i])
                i += 1
                yield arr.copy(), {'left': i}, 14  # Line 14: i += 1
            else:
                yield arr.copy(), {'right': j}, 15  # Line 15: else
                merged.append(arr[j])
                j += 1
                yield arr.copy(), {'right': j}, 17  # Line 17: j += 1
        while i <= mid:
            yield arr.copy(), {'left': i}, 18  # Line 18: while i <= mid
            merged.append(arr[i])
            i += 1
            yield arr.copy(), {'left': i}, 20  # Line 20: i += 1
        while j <= right:
            yield arr.copy(), {'right': j}, 21  # Line 21: while j <= right
            merged.append(arr[j])
            j += 1
            yield arr.copy(), {'right': j}, 23  # Line 23: j += 1
        for k, val in enumerate(merged):
            arr[left + k] = val
            yield arr.copy(), {'merged': left + k}, 24  # Line 24: for k, val in enumerate(merged)

    def quick_sort_generator(self, arr, low, high):
        """Generator for quick sort algorithm visualization."""
        yield arr.copy(), {}, 1  # Line 1: def quick_sort...
        if low < high:
            yield arr.copy(), {}, 2  # Line 2: if low < high...
            yield arr.copy(), {}, 3  # Line 3: pi = partition(arr, low, high)
            pi = yield from self.partition_generator(arr, low, high)
            yield arr.copy(), {}, 4  # Line 4: quick_sort(arr, low, pi - 1)
            yield from self.quick_sort_generator(arr, low, pi - 1)
            yield arr.copy(), {}, 5  # Line 5: quick_sort(arr, pi + 1, high)
            yield from self.quick_sort_generator(arr, pi + 1, high)
        else:
            return

    def partition_generator(self, arr, low, high):
        """Generator for partitioning in quick sort."""
        yield arr.copy(), {}, 6   # Line 6: def partition...
        pivot = arr[high]
        yield arr.copy(), {'pivot': high}, 7  # Line 7: pivot = arr[high]
        i = low
        yield arr.copy(), {}, 8   # Line 8: i = low
        for j in range(low, high):
            yield arr.copy(), {'i': i, 'j': j, 'pivot': high}, 9  # Line 9: for j in range(low, high)
            if arr[j] < pivot:
                yield arr.copy(), {'i': i, 'j': j, 'pivot': high}, 10  # Line 10: if arr[j] < pivot
                arr[i], arr[j] = arr[j], arr[i]
                yield arr.copy(), {'swap': [i, j], 'pivot': high}, 11  # Line 11: arr[i], arr[j] = arr[j], arr[i]
                i += 1
                yield arr.copy(), {'i': i, 'pivot': high}, 12  # Line 12: i += 1
        arr[i], arr[high] = arr[high], arr[i]
        yield arr.copy(), {'swap': [i, high]}, 13  # Line 13: arr[i], arr[high] = arr[high], arr[i]
        yield arr.copy(), {}, 14  # Line 14: return i
        return i

    def binary_search_generator(self, arr, target):
        """Generator for binary search algorithm visualization."""
        yield arr.copy(), {'target': target}, 1  # Line 1
        left = 0
        yield arr.copy(), {'left': left}, 2      # Line 2
        right = len(arr) - 1
        yield arr.copy(), {'right': right}, 3    # Line 3
        while left <= right:
            yield arr.copy(), {'left': left, 'right': right}, 4  # Line 4
            mid = (left + right) // 2
            yield arr.copy(), {'mid': mid}, 5    # Line 5
            if arr[mid] == target:
                yield arr.copy(), {'mid': mid}, 6  # Line 6
                yield arr.copy(), {'found': mid}, 7  # Line 7
                return
            elif arr[mid] < target:
                yield arr.copy(), {'mid': mid}, 8   # Line 8
                left = mid + 1
                yield arr.copy(), {'left': left}, 9  # Line 9
            else:
                yield arr.copy(), {'mid': mid}, 10  # Line 10
                right = mid -1
                yield arr.copy(), {'right': right}, 11  # Line 11
        yield arr.copy(), {}, 12  # Line 12

    def precompute_frames(self):
        """Precomputes the frames for the sorting animations."""
        self.precomputed_frames['merge'] = list(self.merge_sort_generator(self.array.copy(), 0, len(self.array) - 1))
        self.precomputed_frames['quick'] = list(self.quick_sort_generator(self.array.copy(), 0, len(self.array) - 1))
        self.precomputed_frames['binary'] = list(self.binary_search_generator(self.array.copy(), self.target_value))
        self.frames = self.precomputed_frames[self.algorithm]

    def animate(self):
        """Starts the animation of the sorting visualization."""
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update,
            frames=range(len(self.frames)),
            interval=self.interval * 1000,  # Convert to milliseconds
            repeat=False,
            blit=False,
        )
        plt.show()

    def update(self, frame_number):
        """Updates the plot for each frame in the animation."""
        self.current_frame = frame_number  # Keep track of the current frame
        data = self.frames[frame_number]
        arr, color_indices, line_number = data

        # Update bar heights and reset colors
        for rect, val in zip(self.bar_rects, arr):
            rect.set_height(val)
            rect.set_color('lightblue')

        if self.algorithm == 'binary':
            # Gray out elements outside the current search range
            if 'left' in color_indices and 'right' in color_indices:
                for i in range(len(arr)):
                    if i < color_indices['left'] or i > color_indices['right']:
                        self.bar_rects[i].set_color('grey')
            # Highlight the middle element
            if 'mid' in color_indices:
                self.bar_rects[color_indices['mid']].set_color('yellow')
            # Highlight the found element
            if 'found' in color_indices:
                self.bar_rects[color_indices['found']].set_color('green')
                # Pause the animation upon finding the target
                self.ani.event_source.stop()
        else:
            # Highlight specific bars based on sorting algorithm steps
            if 'pivot' in color_indices:
                pivot_index = color_indices['pivot']
                self.bar_rects[pivot_index].set_color('yellow')
            if 'i' in color_indices and 'j' in color_indices:
                self.bar_rects[color_indices['i']].set_color('red')
                self.bar_rects[color_indices['j']].set_color('green')
            if 'swap' in color_indices:
                for index in color_indices['swap']:
                    self.bar_rects[index].set_color('orange')
            if 'merged' in color_indices:
                self.bar_rects[color_indices['merged']].set_color('purple')
            if 'left' in color_indices:
                self.bar_rects[color_indices['left']].set_color('red')
            if 'right' in color_indices:
                self.bar_rects[color_indices['right']].set_color('green')

        # Update pseudocode highlighting and operation count
        self.pseudocode_display.highlight_line(line_number)
        self.operations = frame_number  # Update operations count based on frame number
        self.operation_text.set_text(f"Operations: {self.operations}")
        self.slider.set_val(frame_number)
        self.fig.canvas.draw_idle()

    def slider_update(self, val):
        """Updates the frame when the slider is moved."""
        frame_number = int(self.slider.val)
        self.update(frame_number)

    def toggle_pause(self, event):
        """Pauses or resumes the animation."""
        if self.paused:
            self.ani.event_source.start()
            self.button.label.set_text('Pause')
        else:
            self.ani.event_source.stop()
            self.button.label.set_text('Play')
        self.paused = not self.paused

    def submit_speed(self, event):
        """Updates the animation speed based on user input."""
        speed_str = self.speed_text_box.text
        try:
            new_interval = float(speed_str)
            if new_interval > 0:
                self.interval = new_interval
                self.update_speed()
            else:
                print("Please enter a positive number for speed.")
        except ValueError:
            print("Invalid input for speed. Please enter a number.")

    def update_speed(self):
        """Applies the new animation speed."""
        self.ani.event_source.interval = self.interval * 1000
        self.restart_animation(None)

    def restart_animation(self, event):
        """Restarts the animation from the beginning."""
        # Regenerate the array based on the algorithm
        if self.algorithm == 'binary':
            # Use a larger array for binary search
            self.array = np.random.randint(1, 1000, size=1000)
            self.array.sort()
            self.target_value = self.array[len(self.array) // 2]
        else:
            # Use the original unsorted array
            self.array = self.original_array.copy()
        
        # Update the bar heights and reset colors
        self.ax.clear()
        self.bar_rects = self.ax.bar(range(len(self.array)), self.array, align="edge", color='lightblue')
        self.ax.set_xlim(0, len(self.array))
        self.ax.set_ylim(0, int(max(self.array) * 1.1))
        for rect, val in zip(self.bar_rects, self.array):
            rect.set_height(val)
            rect.set_color('lightblue')
        
        # Reset the operation counter and text display
        self.operations = 0
        self.operation_text.set_text(f"Operations: {self.operations}")
        
        # Recompute frames
        self.precompute_frames()
        self.frames = self.precomputed_frames[self.algorithm]
        
        # Reset the slider
        self.slider.valmax = len(self.frames) - 1
        self.slider.ax.set_xlim(self.slider.valmin, self.slider.valmax)
        self.slider.set_val(0)
        self.current_frame = 0
        
        # Reset pseudocode highlighting
        self.pseudocode_display.highlight_line(0)
        
        # Restart the animation
        self.ani.event_source.stop()
        self.ani.new_frame_seq()
        if not self.paused:
            self.ani.event_source.start()

    def update_algorithm(self, label):
        """Changes the sorting algorithm and updates the visualization."""
        self.algorithm = label
        self.define_pseudocode()
        self.pseudocode_display.update_code(self.pseudocode)
        
        # Regenerate the array based on the algorithm
        if self.algorithm == 'binary':
            # Use a larger array for binary search
            self.array = np.random.randint(1, 1000, size=1000)
            self.array.sort()
            self.target_value = self.array[len(self.array) // 2]
        else:
            # Use the original array for other algorithms
            self.array = self.original_array.copy()
        
        # Update the bar plot
        self.ax.clear()
        self.bar_rects = self.ax.bar(range(len(self.array)), self.array, align="edge", color='lightblue')
        self.ax.set_xlim(0, len(self.array))
        self.ax.set_ylim(0, int(max(self.array) * 1.1))
        self.ax.set_title(f"{self.algorithm.capitalize()} Visualization")
        self.ax.set_xlabel("Index")
        self.ax.set_ylabel("Value")
        
        # Recompute frames and restart animation
        self.restart_animation(None)

    def setup_gui(self):
        """Sets up the GUI components and event handlers."""
        # Slider for frame navigation
        ax_slider = plt.axes([0.13, 0.15, 0.65, 0.03])
        self.slider = Slider(ax_slider, 'Frame', 0, len(self.frames) - 1, valinit=0, valfmt='%0.0f')

        # Pause/Play button
        ax_button = plt.axes([0.83, 0.15, 0.1, 0.04])
        self.button = Button(ax_button, 'Pause')

        # Step Forward button
        ax_step_forward = plt.axes([0.83, 0.10, 0.1, 0.04])
        self.step_forward_button = Button(ax_step_forward, 'Step Forward')

        # Step Backward button
        ax_step_backward = plt.axes([0.72, 0.10, 0.1, 0.04])
        self.step_backward_button = Button(ax_step_backward, 'Step Backward')

        # Text box for speed input
        ax_speed_text = plt.axes([0.13, 0.05, 0.45, 0.03])
        self.speed_text_box = TextBox(ax_speed_text, 'Speed (s):', initial=str(self.interval))

        # 'Update Speed' button to apply new speed
        ax_run_button = plt.axes([0.6, 0.05, 0.1, 0.04])
        self.run_button = Button(ax_run_button, 'Update Speed')

        # 'Restart' button to restart the animation
        ax_restart_button = plt.axes([0.72, 0.05, 0.1, 0.04])
        self.restart_button = Button(ax_restart_button, 'Restart')

        # Radio buttons for algorithm selection
        ax_algo = plt.axes([0.025, 0.5, 0.1, 0.2])
        self.algo_radio = RadioButtons(ax_algo, ('merge', 'quick', 'binary'))

        # Text box for target value input (only for binary search)
        ax_target_text = plt.axes([0.13, 0.01, 0.45, 0.03])
        self.target_text_box = TextBox(ax_target_text, 'Target Value:', initial=str(self.target_value))
        self.target_text_box.on_submit(self.update_target_value)

        # Connect event handlers
        self.slider.on_changed(self.slider_update)
        self.button.on_clicked(self.toggle_pause)
        self.run_button.on_clicked(self.submit_speed)
        self.restart_button.on_clicked(self.restart_animation)
        self.algo_radio.on_clicked(self.update_algorithm)
        self.step_forward_button.on_clicked(self.step_forward)
        self.step_backward_button.on_clicked(self.step_backward)

    def update_target_value(self, text):
        """Updates the target value for binary search."""
        try:
            self.target_value = int(text)
            self.restart_animation(None)
        except ValueError:
            print("Please enter a valid integer for the target value.")

    def step_forward(self, event):
        """Steps forward one frame in the animation."""
        if self.current_frame < len(self.frames) - 1:
            self.current_frame += 1
            self.update(self.current_frame)

    def step_backward(self, event):
        """Steps backward one frame in the animation."""
        if self.current_frame > 0:
            self.current_frame -= 1
            self.update(self.current_frame)

if __name__ == "__main__":
    array = np.random.randint(1, 100, size=50)
    visualizer = SortVisualizer(array)
    visualizer.animate()