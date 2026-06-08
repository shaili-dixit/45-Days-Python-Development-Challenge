"""
Graph Traversal Engine with BFS, DFS, Shortest Path and Cycle Detection
Adjacency list representation; BFS, DFS, shortest path, cycle detection.
"""

from collections import defaultdict, deque


class Graph:
    def __init__(self, directed=False):
        self.adj = defaultdict(list)
        self.directed = directed
        self.nodes = set()

    def add_edge(self, u, v, weight=1):
        self.adj[u].append((v, weight))
        self.nodes.add(u)
        self.nodes.add(v)
        if not self.directed:
            self.adj[v].append((u, weight))

    def add_node(self, u):
        self.nodes.add(u)
        if u not in self.adj:
            self.adj[u] = []

    def neighbors(self, node):
        return [v for v, _ in self.adj[node]]

    def weighted_neighbors(self, node):
        return self.adj[node]

    # ── BFS ────────────────────────────────────────────────────────
    def bfs(self, start, verbose=True):
        if start not in self.nodes:
            print(f"  Node '{start}' not in graph.")
            return []

        visited = set()
        queue = deque([start])
        order = []
        parent = {start: None}
        level = {start: 0}

        while queue:
            node = queue.popleft()
            if node in visited:
                continue
            visited.add(node)
            order.append(node)

            for neighbor in sorted(self.neighbors(node)):
                if neighbor not in visited:
                    queue.append(neighbor)
                    if neighbor not in parent:
                        parent[neighbor] = node
                        level[neighbor] = level[node] + 1

        if verbose:
            print(f"\n  BFS from '{start}': {' → '.join(str(n) for n in order)}")
            for node in order:
                print(f"    {node}: level={level.get(node, '?')}, parent={parent.get(node)}")
        return order

    # ── DFS ────────────────────────────────────────────────────────
    def dfs(self, start, verbose=True):
        if start not in self.nodes:
            return []
        visited = set()
        order = []
        entry = {}
        exit_ = {}
        self._timer = [0]

        def dfs_visit(node):
            visited.add(node)
            entry[node] = self._timer[0]
            self._timer[0] += 1
            order.append(node)
            for neighbor in sorted(self.neighbors(node)):
                if neighbor not in visited:
                    dfs_visit(neighbor)
            exit_[node] = self._timer[0]
            self._timer[0] += 1

        dfs_visit(start)

        if verbose:
            print(f"\n  DFS from '{start}': {' → '.join(str(n) for n in order)}")
            for node in order:
                print(f"    {node}: entry={entry[node]}, exit={exit_[node]}")
        return order

    # ── Shortest Path (BFS, unweighted) ───────────────────────────
    def shortest_path(self, start, end):
        if start not in self.nodes or end not in self.nodes:
            return None, float('inf')

        visited = {start}
        queue = deque([[start]])

        while queue:
            path = queue.popleft()
            node = path[-1]
            if node == end:
                return path, len(path) - 1
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append(path + [neighbor])

        return None, float('inf')

    # ── Dijkstra Shortest Path (weighted) ─────────────────────────
    def dijkstra(self, start):
        import heapq
        dist = {node: float('inf') for node in self.nodes}
        prev = {node: None for node in self.nodes}
        dist[start] = 0
        heap = [(0, start)]

        while heap:
            d, node = heapq.heappop(heap)
            if d > dist[node]:
                continue
            for neighbor, weight in self.weighted_neighbors(node):
                nd = dist[node] + weight
                if nd < dist[neighbor]:
                    dist[neighbor] = nd
                    prev[neighbor] = node
                    heapq.heappush(heap, (nd, neighbor))

        return dist, prev

    def dijkstra_path(self, start, end):
        dist, prev = self.dijkstra(start)
        if dist[end] == float('inf'):
            return None, float('inf')
        path = []
        node = end
        while node is not None:
            path.append(node)
            node = prev[node]
        return list(reversed(path)), dist[end]

    # ── Cycle Detection ────────────────────────────────────────────
    def has_cycle(self):
        visited = set()
        rec_stack = set()

        def dfs_cycle(node):
            visited.add(node)
            rec_stack.add(node)
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    if dfs_cycle(neighbor):
                        return True
                elif self.directed and neighbor in rec_stack:
                    return True
                elif not self.directed and neighbor in visited:
                    pass  # handled separately for undirected
            rec_stack.discard(node)
            return False

        if self.directed:
            for node in list(self.nodes):
                if node not in visited:
                    if dfs_cycle(node):
                        return True
            return False
        else:
            return self._has_cycle_undirected()

    def _has_cycle_undirected(self):
        visited = set()

        def dfs(node, parent):
            visited.add(node)
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    if dfs(neighbor, node):
                        return True
                elif neighbor != parent:
                    return True
            return False

        for node in list(self.nodes):
            if node not in visited:
                if dfs(node, None):
                    return True
        return False

    def connected_components(self):
        visited = set()
        components = []

        def dfs(node, comp):
            visited.add(node)
            comp.append(node)
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    dfs(neighbor, comp)

        for node in sorted(self.nodes):
            if node not in visited:
                comp = []
                dfs(node, comp)
                components.append(sorted(comp))

        return components

    def topological_sort(self):
        if not self.directed:
            return None
        visited = set()
        stack = []

        def dfs(node):
            visited.add(node)
            for neighbor in self.neighbors(node):
                if neighbor not in visited:
                    dfs(neighbor)
            stack.append(node)

        for node in list(self.nodes):
            if node not in visited:
                dfs(node)
        return list(reversed(stack))


def demo():
    print("\n  ── Undirected Graph Demo ──")
    g = Graph(directed=False)
    edges = [('A','B'), ('A','C'), ('B','D'), ('B','E'), ('C','F'), ('D','E'), ('E','F')]
    for u, v in edges:
        g.add_edge(u, v)

    g.bfs('A')
    g.dfs('A')

    for start, end in [('A','F'), ('B','C'), ('A','D')]:
        path, dist = g.shortest_path(start, end)
        print(f"\n  Shortest path {start}→{end}: {' → '.join(path)}  (length={dist})")

    print(f"\n  Has cycle: {g.has_cycle()}")
    print(f"  Connected components: {g.connected_components()}")

    print("\n  ── Directed Graph (Topological Sort) ──")
    dag = Graph(directed=True)
    dag_edges = [('A','C'), ('B','C'), ('B','D'), ('C','E'), ('D','F'), ('E','F')]
    for u, v in dag_edges:
        dag.add_edge(u, v)
    print(f"  Topological order: {dag.topological_sort()}")
    print(f"  Has cycle: {dag.has_cycle()}")

    # Cycle test
    print("\n  ── Directed Graph with Cycle ──")
    cyclic = Graph(directed=True)
    for u, v in [('A','B'), ('B','C'), ('C','A')]:
        cyclic.add_edge(u, v)
    print(f"  Has cycle: {cyclic.has_cycle()}")

    print("\n  ── Weighted Graph (Dijkstra) ──")
    wg = Graph(directed=False)
    weighted_edges = [
        ('A','B',4), ('A','C',2), ('B','C',1), ('B','D',5),
        ('C','D',8), ('C','E',10), ('D','E',2), ('D','F',6), ('E','F',3),
    ]
    for u, v, w in weighted_edges:
        wg.add_edge(u, v, w)

    dist, _ = wg.dijkstra('A')
    print(f"  Dijkstra distances from A:")
    for node in sorted(dist):
        print(f"    A → {node}: {dist[node]}")

    path, cost = wg.dijkstra_path('A', 'F')
    print(f"\n  Optimal path A→F: {' → '.join(path)}  (cost={cost})")


def main():
    print("╔══════════════════════════════════════════╗")
    print("║   Graph Traversal Engine v1.0           ║")
    print("╚══════════════════════════════════════════╝")
    demo()


if __name__ == "__main__":
    main()
