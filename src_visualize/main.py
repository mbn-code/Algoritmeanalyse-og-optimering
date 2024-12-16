import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.widgets import Slider, Button, RadioButtons, TextBox
from matplotlib.gridspec import GridSpec
from numba import jit
import sys
sys.setrecursionlimit(1500)

class PseudoCodeDisplay:
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
    def __init__(self, array):
        self.array = array.copy()
        self.operations = 0
        self.algorithm = "merge"
        self.interval = 0.05  # Set default interval to 0.05 seconds for faster animation
        self.paused = False
        self.frames = []
        self.precomputed_frames = {}

        # Adjust layout to accommodate pseudocode display and GUI elements
        self.fig = plt.figure(figsize=(12, 6))
        gs = GridSpec(1, 2, width_ratios=[3, 1])
        self.ax = self.fig.add_subplot(gs[0])
        self.pseudo_ax = self.fig.add_subplot(gs[1])
        plt.subplots_adjust(bottom=0.3, right=0.75)

        self.bar_rects = self.ax.bar(range(len(self.array)), self.array, align="edge", color='lightblue')
        self.ax.set_xlim(0, len(self.array))
        self.ax.set_ylim(0, int(max(self.array) * 1.1))
        self.text = self.ax.text(0.02, 0.95, "", transform=self.ax.transAxes)

        # Create legend patches
        legend_patches = [
            mpatches.Patch(color='lightblue', label='Unsorted elements'),
            mpatches.Patch(color='yellow', label='Pivot element'),
            mpatches.Patch(color='red', label='Low/Left index'),
            mpatches.Patch(color='green', label='High/Right index'),
            mpatches.Patch(color='orange', label='Swapped elements'),
            mpatches.Patch(color='purple', label='Merged elements'),
        ]
        self.ax.legend(handles=legend_patches, loc='upper right')

        # Define simplified pseudocode for the selected algorithm
        self.define_pseudocode()

        # Initialize pseudocode display
        self.pseudocode_display = PseudoCodeDisplay(self.pseudo_ax, self.pseudocode)

        # Precompute all frames for both algorithms
        self.precompute_frames()

        # Slider for frame navigation
        ax_slider = plt.axes([0.13, 0.1, 0.65, 0.03])
        self.slider = Slider(ax_slider, 'Frame', 0, len(self.frames) - 1, valinit=0, valfmt='%0.0f')

        # Pause/Play button
        ax_button = plt.axes([0.83, 0.1, 0.1, 0.04])
        self.button = Button(ax_button, 'Pause')

        # Text box for speed input in seconds
        ax_speed_text = plt.axes([0.13, 0.05, 0.45, 0.03])
        self.speed_text_box = TextBox(ax_speed_text, 'Speed (s):', initial=str(self.interval))

        # 'Run' button to apply new speed
        ax_run_button = plt.axes([0.6, 0.05, 0.1, 0.04])
        self.run_button = Button(ax_run_button, 'Run')

        # 'Restart' button to restart the animation
        ax_restart_button = plt.axes([0.72, 0.05, 0.1, 0.04])
        self.restart_button = Button(ax_restart_button, 'Restart')

        # Radio buttons for algorithm selection
        ax_algo = plt.axes([0.025, 0.4, 0.1, 0.15])
        self.algo_radio = RadioButtons(ax_algo, ('merge', 'quick'))

        # Connect events
        self.slider.on_changed(self.slider_update)
        self.button.on_clicked(self.toggle_pause)
        self.run_button.on_clicked(self.submit_speed)
        self.restart_button.on_clicked(self.restart_animation)
        self.algo_radio.on_clicked(self.update_algorithm)

    def define_pseudocode(self):
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
        self.precomputed_frames['merge'] = []
        self.precomputed_frames['quick'] = []

        # Precompute frames for merge sort
        generator = self.merge_sort_generator(self.array.copy(), 0, len(self.array) - 1)
        for frame in generator:
            self.precomputed_frames['merge'].append(frame)

        # Precompute frames for quick sort
        generator = self.quick_sort_generator(self.array.copy(), 0, len(self.array) - 1)
        for frame in generator:
            self.precomputed_frames['quick'].append(frame)

        # Set initial frames to merge sort
        self.frames = self.precomputed_frames['merge']

    def merge_sort_generator(self, arr, left, right):
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
        yield arr.copy(), {}, 1  # Line 1: def quick_sort...
        if low < high:
            yield arr.copy(), {}, 2  # Line 2: if low < high...
            pi = yield from self.partition_generator(arr, low, high)
            yield from self.quick_sort_generator(arr, low, pi - 1)
            yield from self.quick_sort_generator(arr, pi + 1, high)
        else:
            yield arr.copy(), {}, 5  # Line 5: else (do nothing)

    def partition_generator(self, arr, low, high):
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

    @jit(nopython=True)
    def merge_sort(self, arr, left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        self.merge_sort(arr, left, mid)
        self.merge_sort(arr, mid + 1, right)
        self.merge(arr, left, mid, right)

    @jit(nopython=True)
    def merge(self, arr, left, mid, right):
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

    @jit(nopython=True)
    def quick_sort(self, arr, low, high):
        if low < high:
            pi = self.partition(arr, low, high)
            self.quick_sort(arr, low, pi - 1)
            self.quick_sort(arr, pi + 1, high)

    @jit(nopython=True)
    def partition(self, arr, low, high):
        pivot = arr[high]
        i = low
        for j in range(low, high):
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                i += 1
        arr[i], arr[high] = arr[high], arr[i]
        return i

    def animate(self):
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update,
            frames=range(len(self.frames)),
            interval=self.interval * 1000,  # Convert seconds to milliseconds
            repeat=False,
            blit=False,
        )
        plt.show()

    def update(self, frame_number):
        data = self.frames[frame_number]
        arr = data[0]
        color_indices = data[1]
        line_number = data[2]  # Line number for pseudocode highlighting

        for rect, val in zip(self.bar_rects, arr):
            rect.set_height(val)
            rect.set_color('lightblue')

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

        self.pseudocode_display.highlight_line(line_number)

        self.text.set_text(f"Operations: {self.operations}")
        self.slider.set_val(frame_number)
        self.fig.canvas.draw_idle()

    def slider_update(self, val):
        frame_number = int(self.slider.val)
        self.update(frame_number)
        self.fig.canvas.draw_idle()

    def toggle_pause(self, event):
        if self.paused:
            self.ani.event_source.start()
            self.button.label.set_text('Pause')
        else:
            self.ani.event_source.stop()
            self.button.label.set_text('Play')
        self.paused = not self.paused

    def submit_speed(self, event):
        # Get the speed input from the text box
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
        # Update the animation interval
        self.ani.event_source.interval = self.interval * 1000  # Update animation interval
        # Restart the animation
        self.restart_animation(None)

    def restart_animation(self, event):
        # Restart the animation
        self.ani.event_source.stop()
        self.ani.new_frame_seq()
        self.slider.set_val(0)
        if not self.paused:
            self.ani.event_source.start()

    def update_algorithm(self, label):
        self.algorithm = label
        # Update pseudocode
        self.define_pseudocode()
        self.pseudocode_display.update_code(self.pseudocode)

        # Use precomputed frames for the selected algorithm
        self.frames = self.precomputed_frames[self.algorithm]

        # Update slider
        self.slider.valmax = len(self.frames) - 1
        self.slider.ax.set_xlim(self.slider.valmin, self.slider.valmax)
        self.slider.set_val(0)

        # Restart animation
        self.restart_animation(None)

if __name__ == "__main__":
    array = np.random.randint(1, 100, size=50)
    visualizer = SortVisualizer(array)
    visualizer.animate()