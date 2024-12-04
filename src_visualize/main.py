import matplotlib.pyplot as plt
import matplotlib.animation as animation
import matplotlib.patches as mpatches
import numpy as np
from matplotlib.widgets import Slider, Button
from matplotlib.gridspec import GridSpec

class SortVisualizer:
    def __init__(self, array, algorithm="merge", interval=0.5):
        self.array = array.copy()
        self.operations = 0
        self.algorithm = algorithm
        self.interval = interval  # Interval in seconds
        self.paused = False
        self.frames = []

        self.fig, self.ax = plt.subplots(figsize=(12, 6))
        plt.subplots_adjust(bottom=0.25)  # Make space for slider and buttons
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

        # Compute all frames beforehand
        self.compute_frames()

        # Slider axis
        ax_slider = plt.axes([0.13, 0.1, 0.65, 0.03])
        self.slider = Slider(ax_slider, 'Frame', 0, len(self.frames)-1, valinit=0, valfmt='%0.0f')

        # Pause/Play button
        ax_button = plt.axes([0.83, 0.1, 0.1, 0.04])
        self.button = Button(ax_button, 'Pause')

        # Connect events
        self.slider.on_changed(self.slider_update)
        self.button.on_clicked(self.toggle_pause)

    def compute_frames(self):
        if self.algorithm == "merge":
            generator = self.merge_sort(self.array.copy(), 0, len(self.array) - 1)
        elif self.algorithm == "quick":
            generator = self.quick_sort(self.array.copy(), 0, len(self.array) - 1)
        for frame in generator:
            self.frames.append(frame)

    def merge_sort(self, arr, left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        yield from self.merge_sort(arr, left, mid)
        yield from self.merge_sort(arr, mid + 1, right)
        yield from self.merge(arr, left, mid, right)

    def merge(self, arr, left, mid, right):
        merged = []
        i, j = left, mid + 1
        while i <= mid and j <= right:
            self.operations += 1
            yield arr.copy(), {'left': i, 'right': j}
            if arr[i] <= arr[j]:
                merged.append(arr[i])
                i += 1
            else:
                merged.append(arr[j])
                j += 1
        while i <= mid:
            merged.append(arr[i])
            i += 1
            yield arr.copy(), {'left': i}
        while j <= right:
            merged.append(arr[j])
            j += 1
            yield arr.copy(), {'right': j}
        for k, val in enumerate(merged):
            arr[left + k] = val
            yield arr.copy(), {'merged': left + k}

    def quick_sort(self, arr, low, high):
        if low < high:
            pivot_index = yield from self.partition(arr, low, high)
            yield from self.quick_sort(arr, low, pivot_index - 1)
            yield from self.quick_sort(arr, pivot_index + 1, high)

    def partition(self, arr, low, high):
        pivot = arr[high]
        i = low
        yield arr.copy(), {'pivot': high}
        for j in range(low, high):
            self.operations += 1
            yield arr.copy(), {'i': i, 'j': j, 'pivot': high}
            if arr[j] < pivot:
                arr[i], arr[j] = arr[j], arr[i]
                yield arr.copy(), {'swap': [i, j], 'pivot': high}
                i += 1
        arr[i], arr[high] = arr[high], arr[i]
        yield arr.copy(), {'swap': [i, high], 'pivot': high}
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
        arr, color_indices = data
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

        self.text.set_text(f"Operations: {self.operations}")
        self.slider.set_val(frame_number)

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

if __name__ == "__main__":
    np.random.seed(0)
    arr_size = 30
    arr = np.random.randint(1, 100, arr_size)
    algorithm = input("Choose algorithm (merge/quick): ").strip().lower()
    speed = float(input("Set animation speed (seconds per frame): "))
    viz = SortVisualizer(arr, algorithm=algorithm, interval=speed)
    viz.animate()
    # Add pseudocode display alongside the visualization


    class PseudoCodeDisplay:
        def __init__(self, ax, pseudocode):
            self.ax = ax
            self.code_lines = pseudocode.strip().split('\n')
            self.text_objects = []
            self.highlighted_line = None

            # Display pseudocode lines
            for i, line in enumerate(self.code_lines):
                txt = self.ax.text(0.01, 0.95 - i * 0.05, line, fontsize=10, transform=self.ax.transAxes, ha='left')
                self.text_objects.append(txt)
            self.ax.axis('off')

        def highlight_line(self, line_number):
            # Reset previous highlights
            for txt in self.text_objects:
                txt.set_backgroundcolor('white')
            # Highlight the current line
            if 0 <= line_number < len(self.text_objects):
                self.text_objects[line_number].set_backgroundcolor('yellow')

    # Modify the SortVisualizer class to include pseudocode
    class SortVisualizer:
        def __init__(self, array, algorithm="merge", interval=0.5):
            # Existing initialization code...

            # Adjust layout to accommodate pseudocode display
            self.fig.subplots_adjust(right=0.75)

            # Create subplots for visualization and pseudocode
            gs = GridSpec(1, 2, width_ratios=[3, 1])
            self.ax = self.fig.add_subplot(gs[0])
            self.pseudo_ax = self.fig.add_subplot(gs[1])

            # Define simplified pseudocode for the selected algorithm
            if self.algorithm == "merge":
                pseudocode = '''
    def merge_sort(arr, left, right):
        if left >= right:
            return
        mid = (left + right) // 2
        merge_sort(arr, left, mid)
        merge_sort(arr, mid + 1, right)
        merge(arr, left, mid, right)
    '''
            elif self.algorithm == "quick":
                pseudocode = '''
    def quick_sort(arr, low, high):
        if low < high:
            pi = partition(arr, low, high)
            quick_sort(arr, low, pi - 1)
            quick_sort(arr, pi + 1, high)
    '''

            # Initialize pseudocode display
            self.pseudocode_display = PseudoCodeDisplay(self.pseudo_ax, pseudocode)

            # Rest of the initialization code...

        # Modify the update function to highlight pseudocode lines
        def update(self, frame_number):
            data = self.frames[frame_number]
            arr, color_indices, line_number = data  # line_number indicates the current pseudocode line
            # Update the bars in the bar chart
            for rect, val in zip(self.bar_rects, arr):
                rect.set_height(val)
                rect.set_color('lightblue')

            # Highlight specific bars based on the sorting algorithm's state
            # Existing color update code...

            # Update pseudocode highlighting
            self.pseudocode_display.highlight_line(line_number)

            # Update operation count and slider
            self.text.set_text(f"Operations: {self.operations}")
            self.slider.set_val(frame_number)

        # Modify sorting algorithms to yield the current line number
        def merge_sort(self, arr, left, right):
            yield arr.copy(), {}, 1  # Line 1: def merge_sort...
            if left >= right:
                yield arr.copy(), {}, 2  # Line 2: if left >= right...
                return
            mid = (left + right) // 2
            yield arr.copy(), {}, 3  # Line 3: mid = ...
            yield from self.merge_sort(arr, left, mid)
            yield from self.merge_sort(arr, mid + 1, right)
            yield arr.copy(), {}, 6  # Line 6: merge(arr, left, mid, right)
            yield from self.merge(arr, left, mid, right)

        def quick_sort(self, arr, low, high):
            yield arr.copy(), {}, 1  # Line 1: def quick_sort...
            if low < high:
                yield arr.copy(), {}, 2  # Line 2: if low < high...
                pi = yield from self.partition(arr, low, high)
                yield from self.quick_sort(arr, low, pi - 1)
                yield from self.quick_sort(arr, pi + 1, high)

        # Modify other methods as needed to include line numbers in the yielded data