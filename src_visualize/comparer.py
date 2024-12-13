import pygal
import random
import time
import math

# Python program for implementation of MergeSort
def mergeSort(arr): 
    if len(arr) > 1: 
        mid = len(arr) // 2  # Finding the mid of the array 
        L = arr[:mid]  # Dividing the array elements  
        R = arr[mid:]  # into 2 halves 
  
        mergeSort(L)  # Sorting the first half 
        mergeSort(R)  # Sorting the second half 
  
        i = j = k = 0
          
        # Copy data to temp arrays L[] and R[] 
        while i < len(L) and j < len(R): 
            if L[i] < R[j]: 
                arr[k] = L[i] 
                i += 1
            else: 
                arr[k] = R[j] 
                j += 1
            k += 1
          
        # Checking if any element was left 
        while i < len(L): 
            arr[k] = L[i] 
            i += 1
            k += 1
          
        while j < len(R): 
            arr[k] = R[j] 
            j += 1
            k += 1

# This function takes last element as pivot, places 
# the pivot element at its correct position in sorted 
# array, and places all smaller (smaller than pivot) 
# to left of pivot and all greater elements to right 
# of pivot 
def partition(arr, low, high): 
    i = (low - 1)  # index of smaller element 
    pivot = arr[high]  # pivot 
  
    for j in range(low, high): 
        # If current element is smaller than or equal to pivot 
        if arr[j] <= pivot: 
            i = i + 1 
            arr[i], arr[j] = arr[j], arr[i] 
  
    arr[i + 1], arr[high] = arr[high], arr[i + 1] 
    return (i + 1)

# The main function that implements QuickSort 
def quickSort(arr, low, high): 
    if low < high: 
        # pi is partitioning index, arr[p] is now at right place 
        pi = partition(arr, low, high) 
  
        # Separately sort elements before partition and after partition 
        quickSort(arr, low, pi - 1) 
        quickSort(arr, pi + 1, high)

# Instantiate data sets
xAxis = []
quickSortTime = []
mergeSortTime = []

# Randomly generates an array with the size 10^n for sorting
# Takes the total time of 10 tries of randomly generated arrays
for n in range(0, 5):
    quickSortTotalTime = 0
    mergeSortTotalTime = 0
    for t in range(1, 10):
        # Randomly generates an array with the size 10^n for sorting
        sortThis = [random.randrange(0, 1000000) for _ in range(round(math.pow(10, n)))]
        quickSortThis = sortThis[:]
        mergeSortThis = sortThis[:]
        
        # Time tracking while running the algorithm
        now = int(round(time.time() * 1000))
        quickSort(quickSortThis, 0, len(quickSortThis) - 1)
        deltaTime = int(round(time.time() * 1000)) - now
        quickSortTotalTime += deltaTime
        
        now = int(round(time.time() * 1000))
        mergeSort(mergeSortThis)
        deltaTime = int(round(time.time() * 1000)) - now
        mergeSortTotalTime += deltaTime
    
    # Append tracked time to the data array
    quickSortTime.append(quickSortTotalTime)
    mergeSortTime.append(mergeSortTotalTime)
    xAxis.append(round(math.pow(10, n)))

# Display the data
data = [["Merge Sort", mergeSortTime], ["Quick Sort", quickSortTime]]
line_chart = pygal.Line()
line_chart.title = "Time Comparison between QuickSort & MergeSort"
line_chart.x_labels = map(str, xAxis)
for label, data_points in data:
    line_chart.add(label, data_points)
line_chart.render_in_browser()