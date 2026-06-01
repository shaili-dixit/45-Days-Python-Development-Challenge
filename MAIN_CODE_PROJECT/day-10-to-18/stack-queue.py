"""
Stack and Queue Data Structures Implemented from Scratch with Use Cases
Implements Stack and Queue; solves balanced parentheses; simulates printer queue.
"""

from collections import deque
from datetime import datetime
import time


# ── Stack ──────────────────────────────────────────────────────────────────────
class Stack:
    def __init__(self, name="Stack"):
        self._data = []
        self.name = name

    def push(self, item):
        self._data.append(item)

    def pop(self):
        if self.is_empty():
            raise IndexError("Pop from empty stack")
        return self._data.pop()

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek at empty stack")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def __repr__(self):
        return f"Stack(top→{list(reversed(self._data))})"


# ── Queue ──────────────────────────────────────────────────────────────────────
class Queue:
    def __init__(self, name="Queue", maxsize=None):
        self._data = deque()
        self.name = name
        self.maxsize = maxsize

    def enqueue(self, item):
        if self.maxsize and len(self._data) >= self.maxsize:
            raise OverflowError(f"Queue is full (max {self.maxsize})")
        self._data.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        return self._data.popleft()

    def front(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data[0]

    def rear(self):
        if self.is_empty():
            raise IndexError("Queue is empty")
        return self._data[-1]

    def is_empty(self):
        return len(self._data) == 0

    def size(self):
        return len(self._data)

    def __repr__(self):
        return f"Queue(front→{list(self._data)})"


# ── Balanced Parentheses ───────────────────────────────────────────────────────
PAIRS = {')': '(', ']': '[', '}': '{'}

def check_balanced(expr):
    stack = Stack("Paren Checker")
    for i, ch in enumerate(expr):
        if ch in '([{':
            stack.push((ch, i))
        elif ch in ')]}':
            if stack.is_empty():
                return False, f"Unmatched '{ch}' at position {i}"
            top, pos = stack.pop()
            if top != PAIRS[ch]:
                return False, f"Mismatch: '{top}' at {pos} closed by '{ch}' at {i}"
    if not stack.is_empty():
        ch, pos = stack.peek()
        return False, f"Unclosed '{ch}' at position {pos}"
    return True, "Balanced ✓"


# ── Printer Queue Simulation ───────────────────────────────────────────────────
class PrintJob:
    _counter = 1

    def __init__(self, document, pages, priority=1):
        self.job_id = f"JOB-{PrintJob._counter:04d}"
        PrintJob._counter += 1
        self.document = document
        self.pages = pages
        self.priority = priority  # 1=normal, 2=high, 3=urgent
        self.submitted = datetime.now()
        self.started = None
        self.completed = None

    def __repr__(self):
        return f"PrintJob({self.job_id}, '{self.document}', {self.pages}p)"


class PrinterQueue:
    def __init__(self, name="Printer"):
        self.name = name
        self.queue = Queue(name, maxsize=20)
        self.history = []
        self.total_pages = 0

    def add_job(self, document, pages, priority=1):
        job = PrintJob(document, pages, priority)
        # Insert by priority using temp list (priority queue simulation)
        temp = []
        while not self.queue.is_empty():
            temp.append(self.queue.dequeue())
        temp.append(job)
        temp.sort(key=lambda j: (-j.priority, j.submitted))
        for j in temp:
            self.queue.enqueue(j)
        print(f"  📄 Added: {job.job_id} — '{document}' ({pages} pages) [P{priority}]")
        return job

    def process_next(self):
        if self.queue.is_empty():
            print("  ✓ Queue is empty. Nothing to print.")
            return None
        job = self.queue.dequeue()
        job.started = datetime.now()
        print_time = job.pages * 0.01  # Simulated 0.01s per page
        print(f"  🖨  Printing: {job.job_id} '{job.document}' ({job.pages} pages)...", end=' ')
        time.sleep(min(print_time, 0.1))  # Cap simulation at 0.1s
        job.completed = datetime.now()
        duration = (job.completed - job.started).total_seconds()
        self.total_pages += job.pages
        self.history.append(job)
        print(f"Done! ({duration:.3f}s)")
        return job

    def process_all(self):
        print(f"\n  Processing all jobs in '{self.name}':")
        while not self.queue.is_empty():
            self.process_next()

    def status(self):
        print(f"\n  🖨  Printer: {self.name}")
        print(f"  Jobs in queue : {self.queue.size()}")
        print(f"  Jobs completed: {len(self.history)}")
        print(f"  Total pages   : {self.total_pages}")
        if not self.queue.is_empty():
            print(f"  Next job      : {self.queue.front()}")

    def print_history(self):
        if not self.history:
            print("  No completed jobs.")
            return
        print(f"\n  Print History ({len(self.history)} jobs):")
        print(f"  {'─'*55}")
        for j in self.history:
            wait = (j.started - j.submitted).total_seconds()
            print(f"  {j.job_id}  {j.document:<25} {j.pages:>4}p  Wait: {wait:.3f}s")
        print(f"  {'─'*55}")


def demo_balanced():
    print("\n  ── Balanced Parentheses Checker ──")
    exprs = [
        "{[()]}",
        "((()))",
        "{[(])}",
        "(((",
        "def func(a, b): return (a + b) * [1, 2, 3][0]",
        "}{",
        "",
    ]
    for expr in exprs:
        ok, msg = check_balanced(expr)
        icon = "✓" if ok else "✗"
        print(f"  {icon} \"{expr[:45]:<45}\" → {msg}")


def demo_printer():
    print("\n  ── Printer Queue Simulation ──")
    printer = PrinterQueue("Office Laser Printer")
    printer.add_job("Invoice_Jan.pdf", 5, priority=2)
    printer.add_job("Report_Q4.docx", 50, priority=1)
    printer.add_job("Urgent_Contract.pdf", 10, priority=3)
    printer.add_job("Meeting_Notes.txt", 2, priority=1)
    printer.add_job("Marketing_Plan.pptx", 30, priority=2)
    printer.status()
    printer.process_all()
    printer.print_history()


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Stack & Queue Implementation v1.0     ║")
    print("╚══════════════════════════════════════════╝")

    # Stack demo
    print("\n  ── Stack Demo ──")
    s = Stack()
    for val in [10, 20, 30, 40]:
        s.push(val)
    print(f"  {s}")
    print(f"  Peek: {s.peek()}, Size: {s.size()}")
    print(f"  Pop: {s.pop()}, {s.pop()}")
    print(f"  {s}")

    # Queue demo
    print("\n  ── Queue Demo ──")
    q = Queue(maxsize=5)
    for val in ['A', 'B', 'C', 'D']:
        q.enqueue(val)
    print(f"  {q}")
    print(f"  Front: {q.front()}, Rear: {q.rear()}")
    print(f"  Dequeue: {q.dequeue()}, {q.dequeue()}")
    print(f"  {q}")

    demo_balanced()
    demo_printer()


if __name__ == "__main__":
    main()
