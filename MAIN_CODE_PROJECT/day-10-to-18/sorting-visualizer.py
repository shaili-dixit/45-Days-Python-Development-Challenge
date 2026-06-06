"""
Sorting Algorithm Visualizer with Step-by-Step Trace and Comparison Counter
Implements Bubble, Selection, Insertion, Merge Sort with counters and trace.
"""

import random
import time
import copy


class SortTracer:
    def __init__(self, arr, algorithm_name):
        self.original = list(arr)
        self.arr = list(arr)
        self.name = algorithm_name
        self.comparisons = 0
        self.swaps = 0
        self.passes = []
        self.steps = []

    def record_pass(self):
        self.passes.append(list(self.arr))

    def compare(self, i, j):
        self.comparisons += 1
        return self.arr[i] > self.arr[j]

    def swap(self, i, j):
        self.swaps += 1
        self.arr[i], self.arr[j] = self.arr[j], self.arr[i]

    def print_trace(self, max_passes=8):
        print(f"\n  ── {self.name} Trace ──")
        print(f"  Original : {self.original}")
        for i, state in enumerate(self.passes[:max_passes], 1):
            print(f"  Pass {i:>3} : {state}")
        if len(self.passes) > max_passes:
            print(f"  ... ({len(self.passes) - max_passes} more passes)")
        print(f"  Final    : {self.arr}")

    def stats(self):
        return {
            'algorithm': self.name,
            'comparisons': self.comparisons,
            'swaps': self.swaps,
            'passes': len(self.passes),
        }


def bubble_sort(arr):
    t = SortTracer(arr, "Bubble Sort")
    n = len(t.arr)
    for i in range(n):
        swapped = False
        for j in range(0, n - i - 1):
            if t.compare(j, j + 1):
                t.swap(j, j + 1)
                swapped = True
        t.record_pass()
        if not swapped:
            break
    return t


def selection_sort(arr):
    t = SortTracer(arr, "Selection Sort")
    n = len(t.arr)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            t.comparisons += 1
            if t.arr[j] < t.arr[min_idx]:
                min_idx = j
        if min_idx != i:
            t.swap(i, min_idx)
        t.record_pass()
    return t


def insertion_sort(arr):
    t = SortTracer(arr, "Insertion Sort")
    for i in range(1, len(t.arr)):
        key = t.arr[i]
        j = i - 1
        while j >= 0:
            t.comparisons += 1
            if t.arr[j] > key:
                t.arr[j + 1] = t.arr[j]
                t.swaps += 1
                j -= 1
            else:
                break
        t.arr[j + 1] = key
        t.record_pass()
    return t


def merge_sort_helper(arr, tracer):
    if len(arr) <= 1:
        return arr
    mid = len(arr) // 2
    left = merge_sort_helper(arr[:mid], tracer)
    right = merge_sort_helper(arr[mid:], tracer)
    merged = []
    i = j = 0
    while i < len(left) and j < len(right):
        tracer.comparisons += 1
        if left[i] <= right[j]:
            merged.append(left[i]); i += 1
        else:
            merged.append(right[j]); j += 1
    merged.extend(left[i:])
    merged.extend(right[j:])
    tracer.record_pass()
    return merged


def merge_sort(arr):
    t = SortTracer(arr, "Merge Sort")
    sorted_arr = merge_sort_helper(list(arr), t)
    t.arr = sorted_arr
    t.swaps = 0  # Merge sort uses no swaps, just moves
    return t


def quick_sort_helper(arr, lo, hi, tracer):
    if lo < hi:
        pivot = arr[hi]
        i = lo - 1
        for j in range(lo, hi):
            tracer.comparisons += 1
            if arr[j] <= pivot:
                i += 1
                arr[i], arr[j] = arr[j], arr[i]
                tracer.swaps += 1
        arr[i + 1], arr[hi] = arr[hi], arr[i + 1]
        tracer.swaps += 1
        tracer.record_pass()
        pi = i + 1
        quick_sort_helper(arr, lo, pi - 1, tracer)
        quick_sort_helper(arr, pi + 1, hi, tracer)


def quick_sort(arr):
    t = SortTracer(arr, "Quick Sort")
    quick_sort_helper(t.arr, 0, len(t.arr) - 1, t)
    return t


def compare_algorithms(arr):
    algorithms = [bubble_sort, selection_sort, insertion_sort, merge_sort, quick_sort]
    results = []
    for algo in algorithms:
        input_copy = list(arr)
        start = time.perf_counter()
        tracer = algo(input_copy)
        elapsed = time.perf_counter() - start
        s = tracer.stats()
        s['time_us'] = elapsed * 1_000_000
        results.append(s)
    return results


def print_comparison_table(results):
    print(f"\n  {'═'*72}")
    print(f"  {'Algorithm':<18} {'Comparisons':>13} {'Swaps':>8} {'Passes':>8} {'Time(µs)':>10}")
    print(f"  {'─'*72}")
    for r in sorted(results, key=lambda x: x['comparisons']):
        print(f"  {r['algorithm']:<18} {r['comparisons']:>13,} {r['swaps']:>8,} {r['passes']:>8} {r['time_us']:>10.1f}")
    print(f"  {'═'*72}\n")


def print_all_traces(arr, max_passes=5):
    algorithms = [bubble_sort, selection_sort, insertion_sort, merge_sort]
    for algo in algorithms:
        t = algo(list(arr))
        t.print_trace(max_passes)
        s = t.stats()
        print(f"  → Comparisons: {s['comparisons']}  Swaps: {s['swaps']}  Passes: {s['passes']}\n")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Sorting Algorithm Visualizer v1.0     ║")
    print("╚══════════════════════════════════════════╝")

    small_arr = [64, 34, 25, 12, 22, 11, 90, 45, 7, 55]
    print(f"\n  Input: {small_arr}\n")
    print_all_traces(small_arr, max_passes=6)

    print("\n  Performance Comparison on Various Input Sizes:")
    for size in [10, 100, 500]:
        arr = [random.randint(1, 1000) for _ in range(size)]
        results = compare_algorithms(arr)
        print(f"\n  n = {size} (random):")
        print_comparison_table(results)

    # Already sorted
    arr_sorted = list(range(1, 51))
    print(f"\n  n = 50 (already sorted):")
    results = compare_algorithms(arr_sorted)
    print_comparison_table(results)

    # Reverse sorted
    arr_rev = list(range(50, 0, -1))
    print(f"\n  n = 50 (reverse sorted):")
    results = compare_algorithms(arr_rev)
    print_comparison_table(results)


if __name__ == "__main__":
    main()
