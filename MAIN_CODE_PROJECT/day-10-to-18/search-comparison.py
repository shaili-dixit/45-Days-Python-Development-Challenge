"""
Binary Search vs Linear Search with Performance Comparison and Step Trace
Implements both algorithms with timing, step tracing, and unsorted list handling.
"""

import random
import time
import bisect


class SearchTracer:
    def __init__(self, arr, target, name):
        self.arr = list(arr)
        self.target = target
        self.name = name
        self.steps = []
        self.comparisons = 0
        self.result_index = -1

    def add_step(self, description, current_range=None):
        self.steps.append({'desc': description, 'range': current_range})

    def print_trace(self, max_steps=12):
        print(f"\n  ── {self.name} Trace (target={self.target}) ──")
        for i, step in enumerate(self.steps[:max_steps], 1):
            rng = f"  range={step['range']}" if step['range'] else ""
            print(f"  Step {i:>2}: {step['desc']}{rng}")
        if len(self.steps) > max_steps:
            print(f"  ... ({len(self.steps) - max_steps} more steps)")
        status = f"Found at index {self.result_index}" if self.result_index >= 0 else "Not found"
        print(f"  Result  : {status}")
        print(f"  Comparisons: {self.comparisons}")


def linear_search(arr, target, trace=False):
    t = SearchTracer(arr, target, "Linear Search")
    for i, val in enumerate(arr):
        t.comparisons += 1
        if trace:
            t.add_step(f"Checking arr[{i}]={val}")
        if val == target:
            t.result_index = i
            if trace:
                t.add_step(f"✓ Found {target} at index {i}!")
            return t
    if trace:
        t.add_step(f"✗ {target} not found after {len(arr)} comparisons")
    return t


def binary_search(arr, target, trace=False):
    t = SearchTracer(arr, target, "Binary Search")
    lo, hi = 0, len(arr) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        t.comparisons += 1
        if trace:
            t.add_step(
                f"lo={lo}, hi={hi}, mid={mid}, arr[mid]={arr[mid]}",
                current_range=f"[{lo}..{hi}]"
            )
        if arr[mid] == target:
            t.result_index = mid
            if trace:
                t.add_step(f"✓ Found {target} at index {mid}!")
            return t
        elif arr[mid] < target:
            lo = mid + 1
            if trace:
                t.add_step(f"  {arr[mid]} < {target}, moving lo to {lo}")
        else:
            hi = mid - 1
            if trace:
                t.add_step(f"  {arr[mid]} > {target}, moving hi to {hi}")

    if trace:
        t.add_step(f"✗ {target} not found")
    return t


def binary_search_unsorted(arr, target, trace=False):
    """Binary search on an unsorted list by sorting it first."""
    sorted_arr = sorted(arr)
    t = binary_search(sorted_arr, target, trace)
    t.name = "Binary Search (pre-sorted)"
    t.arr = sorted_arr
    return t


def interpolation_search(arr, target, trace=False):
    """Interpolation search — better than binary for uniformly distributed data."""
    t = SearchTracer(arr, target, "Interpolation Search")
    lo, hi = 0, len(arr) - 1

    while lo <= hi and target >= arr[lo] and target <= arr[hi]:
        if lo == hi:
            t.comparisons += 1
            if arr[lo] == target:
                t.result_index = lo
            return t

        # Estimate position
        pos = lo + int((hi - lo) * (target - arr[lo]) / (arr[hi] - arr[lo]))
        t.comparisons += 1
        if trace:
            t.add_step(f"Estimated pos={pos}, arr[pos]={arr[pos]}")

        if arr[pos] == target:
            t.result_index = pos
            return t
        elif arr[pos] < target:
            lo = pos + 1
        else:
            hi = pos - 1

    return t


def benchmark(arr, target, runs=100):
    """Measure average search time over multiple runs."""
    sorted_arr = sorted(arr)

    def time_it(func, *args):
        start = time.perf_counter()
        for _ in range(runs):
            func(*args)
        return (time.perf_counter() - start) / runs * 1_000_000  # µs

    linear_t = time_it(linear_search, arr, target)
    binary_t = time_it(binary_search, sorted_arr, target)
    interp_t = time_it(interpolation_search, sorted_arr, target)
    bisect_t = time_it(lambda a, x: bisect.bisect_left(a, x), sorted_arr, target)

    return {
        'Linear Search': linear_t,
        'Binary Search': binary_t,
        'Interpolation': interp_t,
        'bisect module':  bisect_t,
    }


def print_benchmark_table(results, n, target):
    print(f"\n  n={n}, target={target}")
    print(f"  {'─'*45}")
    print(f"  {'Algorithm':<22} {'Avg Time (µs)':>14}  {'Speedup':>8}")
    baseline = results.get('Linear Search', 1)
    for algo, t_us in sorted(results.items(), key=lambda x: x[1]):
        speedup = baseline / t_us if t_us > 0 else 0
        print(f"  {algo:<22} {t_us:>14.3f}  {speedup:>7.1f}x")
    print(f"  {'─'*45}")


def demo_trace():
    arr = [3, 7, 12, 19,24, 31,45, 58, 67, 72, 88, 95]
    print(f"\n  Sorted array: {arr}")

    for target in [45, 100]:
        lt = linear_search(arr, target, trace=True)
        lt.print_trace()
        bt = binary_search(arr, target, trace=True)
        bt.print_trace()


def demo_unsorted():
    arr = [64, 34, 25, 12, 22, 11, 90, 45]
    target = 22
    print(f"\n  Unsorted array: {arr}")
    print(f"  Target: {target}")

    lt = linear_search(arr, target, trace=True)
    lt.print_trace()

    bt = binary_search_unsorted(arr, target, trace=True)
    bt.print_trace()


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Search Algorithm Comparison v1.0      ║")
    print("╚══════════════════════════════════════════╝")

    demo_trace()
    demo_unsorted()

    print("\n  Performance Benchmarks:")
    for size in [100, 1000, 10000, 100000]:
        arr = sorted(random.sample(range(size * 2), size))
        target = random.choice(arr)
        results = benchmark(arr, target, runs=200)
        print_benchmark_table(results, size, target)

    # Worst case for linear
    print("\n  Worst-case (target not in array):")
    arr = list(range(0, 10000, 2))  # Even numbers only
    results = benchmark(arr, 9999, runs=200)
    print_benchmark_table(results, len(arr), 9999)


if __name__ == "__main__":
    main()
