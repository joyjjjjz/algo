"""
    Breadth-first search and depth-first search.

    Author: Wenru Dong
"""

from typing import List, Optional, Generator, IO
from collections import deque

class Graph:
    """Undirected graph."""
    def __init__(self, num_vertices):
        self._num_vertices = num_vertices
        self._adjacency = [[] for _ in range(num_vertices)]

        self._found = False

    def add_edge(self, s, t):
        self._adjacency[s].append(t)
        self._adjacency[t].append(s)

    def _generate_path(self, s, t, prev):
        if prev[t] and s != t:
            self._generate_path(s, prev[t], prev)
        print str(t) + ' '

    def bfs(self, s, t):
        """Print out the path from Vertex s to Vertex t
        using bfs.
        """
        if s == t: return

        visited = [False] * self._num_vertices
        visited[s] = True
        q = deque()
        q.append(s)
        prev = [None] * self._num_vertices

        while q:
            v = q.popleft()
            for neighbour in self._adjacency[v]:
                if not visited[neighbour]:
                    prev[neighbour] = v
                    if neighbour == t:
                        print(self._generate_path(s, t, prev))
                        return
                    visited[neighbour] = True
                    q.append(neighbour)

    def dfs(self, s, t):
        """Print out a path from Vertex s to Vertex t
        using dfs.
        """
        visited = [False] * self._num_vertices
        prev = [None] * self._num_vertices
        self._found = False

        def _dfs(from_vertex):
            if self._found:
                return

            visited[from_vertex] = True
            if from_vertex == t:
                self._found = True
                return
            for neighbour in self._adjacency[from_vertex]:
                if not visited[neighbour]:
                    prev[neighbour] = from_vertex
                    _dfs(neighbour)
        
        _dfs(s)
        print(self._generate_path(s, t, prev))


if __name__ == "__main__":
    graph = Graph(8)

    graph.add_edge(0, 1)
    graph.add_edge(0, 3)
    graph.add_edge(1, 2)
    graph.add_edge(1, 4)
    graph.add_edge(2, 5)
    graph.add_edge(3, 4)
    graph.add_edge(4, 5)
    graph.add_edge(4, 6)
    graph.add_edge(5, 7)
    graph.add_edge(6, 7)

    # graph.bfs(0, 7)
    graph.dfs(0, 7)
