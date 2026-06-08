"""
Singly Linked List with Reversal, Cycle Detection and Merge
Full implementation: insert, delete, traverse, reverse, find middle, detect cycle, merge sorted.
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

    def __repr__(self):
        return f"Node({self.data})"


class LinkedList:
    def __init__(self):
        self.head = None
        self._size = 0

    def __len__(self):
        return self._size

    def __repr__(self):
        return f"LinkedList({self.to_list()})"

    # ── Insertion ──────────────────────────────────────────────────
    def prepend(self, data):
        node = Node(data)
        node.next = self.head
        self.head = node
        self._size += 1

    def append(self, data):
        node = Node(data)
        if not self.head:
            self.head = node
        else:
            curr = self.head
            while curr.next:
                curr = curr.next
            curr.next = node
        self._size += 1

    def insert_at(self, index, data):
        if index < 0 or index > self._size:
            raise IndexError(f"Index {index} out of range (size={self._size})")
        if index == 0:
            self.prepend(data)
            return
        node = Node(data)
        curr = self.head
        for _ in range(index - 1):
            curr = curr.next
        node.next = curr.next
        curr.next = node
        self._size += 1

    def insert_sorted(self, data):
        """Insert in sorted (ascending) order."""
        node = Node(data)
        if not self.head or data <= self.head.data:
            node.next = self.head
            self.head = node
        else:
            curr = self.head
            while curr.next and curr.next.data < data:
                curr = curr.next
            node.next = curr.next
            curr.next = node
        self._size += 1

    # ── Deletion ───────────────────────────────────────────────────
    def delete_value(self, data):
        if not self.head:
            return False
        if self.head.data == data:
            self.head = self.head.next
            self._size -= 1
            return True
        curr = self.head
        while curr.next:
            if curr.next.data == data:
                curr.next = curr.next.next
                self._size -= 1
                return True
            curr = curr.next
        return False

    def delete_at(self, index):
        if index < 0 or index >= self._size:
            raise IndexError("Index out of range")
        if index == 0:
            self.head = self.head.next
            self._size -= 1
            return
        curr = self.head
        for _ in range(index - 1):
            curr = curr.next
        curr.next = curr.next.next
        self._size -= 1

    # ── Traversal ──────────────────────────────────────────────────
    def traverse(self):
        curr = self.head
        while curr:
            yield curr.data
            curr = curr.next

    def to_list(self):
        return list(self.traverse())

    def print_list(self, label="List"):
        items = self.to_list()
        chain = " → ".join(str(x) for x in items) + " → NULL"
        print(f"  {label}: {chain}")

    def get(self, index):
        curr = self.head
        for _ in range(index):
            curr = curr.next
        return curr.data if curr else None

    # ── Reverse ────────────────────────────────────────────────────
    def reverse(self):
        prev, curr = None, self.head
        while curr:
            nxt = curr.next
            curr.next = prev
            prev = curr
            curr = nxt
        self.head = prev

    # ── Middle ─────────────────────────────────────────────────────
    def find_middle(self):
        """Floyd's slow/fast pointer to find middle node."""
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
        return slow.data if slow else None

    # ── Cycle Detection ────────────────────────────────────────────
    def has_cycle(self):
        slow = fast = self.head
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                return True
        return False

    def find_cycle_start(self):
        slow = fast = self.head
        has = False
        while fast and fast.next:
            slow = slow.next
            fast = fast.next.next
            if slow is fast:
                has = True
                break
        if not has:
            return None
        slow = self.head
        while slow is not fast:
            slow = slow.next
            fast = fast.next
        return slow.data

    def create_cycle(self, pos):
        """Create a cycle for testing: link last node to node at pos."""
        if self._size == 0:
            return
        nodes = []
        curr = self.head
        while curr:
            nodes.append(curr)
            curr = curr.next
        if 0 <= pos < len(nodes):
            nodes[-1].next = nodes[pos]

    # ── Conversion ─────────────────────────────────────────────────
    @classmethod
    def from_list(cls, lst):
        ll = cls()
        for item in lst:
            ll.append(item)
        return ll

    # ── Nth from End ───────────────────────────────────────────────
    def nth_from_end(self, n):
        ahead = self.head
        behind = self.head
        for _ in range(n):
            if not ahead:
                return None
            ahead = ahead.next
        while ahead:
            ahead = ahead.next
            behind = behind.next
        return behind.data if behind else None


def merge_sorted(l1: LinkedList, l2: LinkedList) -> LinkedList:
    """Merge two sorted linked lists into one sorted list."""
    dummy = Node(0)
    curr = dummy
    a = l1.head
    b = l2.head
    while a and b:
        if a.data <= b.data:
            curr.next = Node(a.data)
            a = a.next
        else:
            curr.next = Node(b.data)
            b = b.next
        curr = curr.next
    while a:
        curr.next = Node(a.data)
        curr = curr.next
        a = a.next
    while b:
        curr.next = Node(b.data)
        curr = curr.next
        b = b.next

    result = LinkedList()
    result.head = dummy.next
    result._size = l1._size + l2._size
    return result


def remove_duplicates(ll: LinkedList) -> LinkedList:
    seen = set()
    curr = ll.head
    prev = None
    while curr:
        if curr.data in seen:
            prev.next = curr.next
            ll._size -= 1
        else:
            seen.add(curr.data)
            prev = curr
        curr = curr.next
    return ll


def demo():
    print("\n  ── Basic Operations ──")
    ll = LinkedList.from_list([10, 20, 30, 40, 50])
    ll.print_list("Original")
    ll.prepend(5)
    ll.append(60)
    ll.insert_at(3, 25)
    ll.print_list("After inserts")

    ll.delete_value(25)
    ll.delete_at(0)
    ll.print_list("After deletes")

    print(f"\n  Middle element: {ll.find_middle()}")
    print(f"  3rd from end  : {ll.nth_from_end(3)}")
    print(f"  Length        : {len(ll)}")

    ll.reverse()
    ll.print_list("Reversed")

    print("\n  ── Sorted Insert ──")
    sl = LinkedList()
    for v in [5, 1, 8, 3, 7, 2]:
        sl.insert_sorted(v)
    sl.print_list("Sorted inserts")

    print("\n  ── Merge Sorted Lists ──")
    l1 = LinkedList.from_list([1, 3, 5, 7, 9])
    l2 = LinkedList.from_list([2, 4, 6, 8, 10])
    l1.print_list("L1")
    l2.print_list("L2")
    merged = merge_sorted(l1, l2)
    merged.print_list("Merged")

    print("\n  ── Cycle Detection ──")
    cyclic = LinkedList.from_list([1, 2, 3, 4, 5])
    print(f"  Normal list has cycle: {cyclic.has_cycle()}")
    cyclic.create_cycle(1)
    print(f"  After creating cycle at pos 1: has_cycle = {cyclic.has_cycle()}")

    print("\n  ── Remove Duplicates ──")
    dup = LinkedList.from_list([1, 2, 3, 2, 4, 3, 5, 1])
    dup.print_list("With duplicates")
    remove_duplicates(dup)
    dup.print_list("After removing duplicates")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Linked List Implementation v1.0       ║")
    print("╚══════════════════════════════════════════╝")
    demo()


if __name__ == "__main__":
    main()
