#!/usr/bin/python
# -*- coding: UTF-8 -*-
import sys

from typing import List, Generator
import heapq


class Graph:
    def __init__(self, vertex_count):
        self.adj = [[] for _ in range(vertex_count)]

    def add_edge(self, s, t, w):
        edge = Edge(s, t, w)
        self.adj[s].append(edge)

    def __len__(self):
        return len(self.adj)


# 下面这个类是为了dijkstra实现用的
class Vertex:
    def __init__(self, v, dist):
        self.id = v         # 顶点编号ID
        self.dist = dist    # 从起始顶点到这个顶点的距离

    def __gt__(self, other):
        return self.dist > other.dist

    def __repr__(self):
        return str((self.id, self.dist))


class Edge:
    def __init__(self, source, target, weight):
        self.s = source
        self.t = target
        self.w = weight


class VertexPriorityQueue:
    def __init__(self):
        self.vertices = []

    def get(self):
        return heapq.heappop(self.vertices)

    def put(self, v):
        self.vertices.append(v)
        self.update_priority()

    def empty(self):
        return len(self.vertices) == 0

    def update_priority(self):
        heapq.heapify(self.vertices)

    def __repr__(self):
        return str(self.vertices)


def dijkstra(g, s, t):
    size = len(g)

    pq = VertexPriorityQueue()  # 节点队列
    in_queue = [False] * size   # 已入队标记
    vertices = [                # 需要随时更新离s的最短距离的节点列表
        Vertex(v, sys.maxint) for v in range(size)
    ]
    predecessor = [-1] * size   # 先驱

    vertices[s].dist = 0
    pq.put(vertices[s])
    in_queue[s] = True

    while not pq.empty():
        v = pq.get()
        if v.id == t:
            break
        for edge in g.adj[v.id]:
            if v.dist + edge.w < vertices[edge.t].dist:
                # 当修改了pq中的元素的优先级后：
                # 1. 有入队操作：触发了pq的堆化，此后出队可以取到优先级最高的顶点
                # 2. 无入队操作：此后出队取到的顶点可能不是优先级最高的，会有bug
                # 为确保正确，需要手动更新一次
                vertices[edge.t].dist = v.dist + edge.w
                predecessor[edge.t] = v.id
                pq.update_priority()        # 更新堆结构
            if not in_queue[edge.t]:
                pq.put(vertices[edge.t])
                in_queue[edge.t] = True

    print_path(s, t, predecessor)
    return vertices[t].dist


def print_path(s, t, p):
    if t == s:
        print(s)
    else:
        print_path(s, p[t], p)
        print t


if __name__ == '__main__':
    g = Graph(6)
    g.add_edge(0, 1, 10)
    g.add_edge(0, 4, 15)
    g.add_edge(1, 2, 15)
    g.add_edge(1, 3, 2)
    g.add_edge(2, 5, 5)
    g.add_edge(3, 2, 1)
    g.add_edge(3, 5, 12)
    g.add_edge(4, 5, 10)
    print(dijkstra(g, 0, 5))

    # 下面这个用例可以暴露更新队列元素优先级的问题
    # g = Graph(4)
    # g.add_edge(0, 1, 18)
    # g.add_edge(0, 2, 3)
    # g.add_edge(2, 1, 1)
    # g.add_edge(1, 3, 5)
    # g.add_edge(2, 3, 8)
    # g.add_edge(0, 3, 15)
    # print(dijkstra(g, 0, 3))
