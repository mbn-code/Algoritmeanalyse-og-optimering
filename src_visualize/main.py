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
        self.algorithm = "quick"
        self.interval = 0.2  # Default interval in seconds
        self.paused = False
        self.frames = []
        self.precomputed_frames = {}

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
        """Defines the pseudocode for the selected sorting algorithm."""
        if self.algorithm == "merge":
            self.pseudocode = '''
def merge_sort(arr, left, right):
    if left >= right:
        return
    mid = (left + right) // 2
    merge_sort(arr, left, mid)
    merge_sort(arr, mid + 1, right)
    merge(arr, left, mid, right)

def merge(arr, left, mid, right):
    merged = []
    i, j = left, mid + 1
    while i <= mid and j <= right:
        if arr[i] <= arr[j]:
            merged.append(arr[i])
            i += 1
        else:
            merged.append(arr[j])
            j += 1
    while i <= mid:
        merged.append(arr[i])
        i += 1
    while j <= right:
        merged.append(arr[j])
        j += 1
    for k, val in enumerate(merged):
        arr[left + k] = val
'''
        elif self.algorithm == "quick":
            self.pseudocode = '''
def quick_sort(arr, low, high):
    if low < high:
        pi = partition(arr, low, high)
        quick_sort(arr, low, pi - 1)
        quick_sort(arr, pi + 1, high)
    else:
        return

def partition(arr, low, high):
    pivot = arr[high]
    i = low
    for j in range(low, high):
        if arr[j] < pivot:
            arr[i], arr[j] = arr[j], arr[i]
            i += 1
    arr[i], arr[high] = arr[high], arr[i]
    return i
'''

    def precompute_frames(self):
        """Precomputes the frames for the sorting animations."""
        self.precomputed_frames['merge'] = list(self.merge_sort_generator(self.array.copy(), 0, len(self.array) - 1))
        self.precomputed_frames['quick'] = list(self.quick_sort_generator(self.array.copy(), 0, len(self.array) - 1))
        self.frames = self.precomputed_frames[self.algorithm]

    def merge_sort_generator(self, arr, left, right):
        """Generator for merge sort algorithm visualization."""
        yield arr.copy(), {}, 1  # Line 1: def merge_sort...
        if left >= right:
            yield arr.copy(), {}, 2  # Line 2: if left >= right...
            return
        mid = (left + right) // 2
        yield arr.copy(), {}, 3  # Line 3: mid = ...
        yield from self.merge_sort_generator(arr, left, mid)
        yield from self.merge_sort_generator(arr, mid + 1, right)
        yield arr.copy(), {}, 6  # Line 6: merge(arr, left, mid, right)
        yield from self.merge_generator(arr, left, mid, right)

    def merge_generator(self, arr, left, mid, right):
        """Generator for merging in merge sort."""
        yield arr.copy(), {}, 7  # Line 7: def merge...
        merged = []
        i, j = left, mid + 1
        yield arr.copy(), {}, 8  # Line 8: i, j initialization
        while i <= mid and j <= right:
            self.operations += 1
            yield arr.copy(), {'left': i, 'right': j}, 9  # Line 9: while i <= mid and j <= right
            if arr[i] <= arr[j]:
                merged.append(arr[i])
                i += 1
                yield arr.copy(), {'left': i}, 10  # Line 10: if arr[i] <= arr[j]
            else:
                merged.append(arr[j])
                j += 1
                yield arr.copy(), {'right': j}, 12  # Line 12: else
        while i <= mid:
            merged.append(arr[i])
            i += 1
            yield arr.copy(), {'left': i}, 14  # Line 14: while i <= mid
        while j <= right:
            merged.append(arr[j])
            j += 1
            yield arr.copy(), {'right': j}, 16  # Line 16: while j <= right
        for k, val in enumerate(merged):
            arr[left + k] = val
            yield arr.copy(), {'merged': left + k}, 18  # Line 18: for k, val in enumerate(merged)

    def quick_sort_generator(self, arr, low, high):
        """Generator for quick sort algorithm visualization."""
        yield arr.copy(), {}, 1  # Line 1: def quick_sort...
        if low < high:
            yield arr.copy(), {}, 2  # Line 2: if low < high...
            pi = yield from self.partition_generator(arr, low, high)
            yield from self.quick_sort_generator(arr, low, pi - 1)
            yield from self.quick_sort_generator(arr, pi + 1, high)
        else:
            yield arr.copy(), {}, 5  # Line 5: else (do nothing)

    def partition_generator(self, arr, low, high):
        """Generator for partitioning in quick sort."""
        yield arr.copy(), {}, 3  # Line 3: def partition...
        pivot = arr[high]
        i = low
        yield arr.copy(), {'pivot': high}, 4  # Line 4: pivot = arr[high]
        for j in range(low, high):
            self.operations += 1
            yield arr.copy(), {'i': i, 'j': j, 'pivot': high}, 5  # Line 5: for j in range(low, high)
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                yield arr.copy(), {'swap': [i, j], 'pivot': high}, 6  # Line 6: if arr[j] < pivot
                i += 1
        arr[i], arr[high] = arr[high], arr[i]
        yield arr.copy(), {'swap': [i, high], 'pivot': high}, 9  # Line 9: arr[i], arr[high] = arr[high], arr[i]
        return i

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
        # Reset the array to its original unsorted state
        self.array = self.original_array.copy()
        self.operations = 0  # Reset the operation counter

        # Update the bar heights and reset colors
        for rect, val in zip(self.bar_rects, self.array):
            rect.set_height(val)
            rect.set_color('lightblue')

        # Reset the text display
        self.operation_text.set_text(f"Operations: {self.operations}")

        # Recompute frames for all algorithms with the new array
        self.precompute_frames()
        self.frames = self.precomputed_frames[self.algorithm]

        # Reset the slider
        self.slider.valmax = len(self.frames) - 1
        self.slider.ax.set_xlim(self.slider.valmin, self.slider.valmax)
        self.slider.set_val(0)
        self.current_frame = 0

        # Reset the pseudocode highlighting
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
        self.frames = self.precomputed_frames[self.algorithm]
        self.slider.valmax = len(self.frames) - 1
        self.slider.ax.set_xlim(self.slider.valmin, self.slider.valmax)
        self.slider.set_val(0)
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
        ax_algo = plt.axes([0.025, 0.5, 0.1, 0.15])
        self.algo_radio = RadioButtons(ax_algo, ('merge', 'quick'))

        # Connect event handlers
        self.slider.on_changed(self.slider_update)
        self.button.on_clicked(self.toggle_pause)
        self.run_button.on_clicked(self.submit_speed)
        self.restart_button.on_clicked(self.restart_animation)
        self.algo_radio.on_clicked(self.update_algorithm)
        self.step_forward_button.on_clicked(self.step_forward)
        self.step_backward_button.on_clicked(self.step_backward)

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