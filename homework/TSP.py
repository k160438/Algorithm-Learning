import numpy as np
import queue

# a function to compute the distance between two points
def distance(a, b):
    return np.sqrt((a[0] - b[0])**2 + (a[1] - b[1])**2)

# a data structure to store covered-path and evaluation function
# state is a number representing a city
# path is a sequence of city numbers
class Node(object):
    def __init__(self, state, f, path, path_cost):
        self.state = state
        self.f = f
        self.path = path
        self.path_cost = path_cost
        return 

    def __lt__(self, other):
        return self.f < other.f

# Generator for TSP, it returns a vertices set and an adjacent matrix
def TSPGenerator(n):
    vertices = np.random.random(size = (n, 2))
    edges = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            edges[i, j] = distance(vertices[i], vertices[j])
            edges[j, i] = edges[i, j]
    return vertices, edges

# MST function, return the minimum of mst
def MST(vertices, edges):
    n = len(vertices)
    mst = 0
    rest_set = vertices[1:]
    mst_set = [vertices[0]]
    while len(mst_set) < n:
        dist = 100000
        for v in mst_set:
            for u in rest_set:
                if edges[v, u] < dist: 
                    dist = edges[v,u]
                    node = u
        mst += dist
        rest_set.remove(node)
        mst_set.append(node)
    return mst

def A_star(n, edges, initial = -1):
    if initial < 0:
        initial = np.random.randint(n)
    q = queue.PriorityQueue()
    q.put(Node(initial, 0, [initial], 0))  # the initial evaluation function doesn't matter
    while not q.empty():
        # print(q.qsize())
        current = q.get()
        # print(current.state, current.path)
        if len(current.path) == n:
            current.path_cost += edges[initial, current.path[-1]]
            return current
        remain = []
        dist_from_init = 100000
        for i in range(n):
            if i not in current.path:
                if edges[initial, i] < dist_from_init:
                    dist_from_init = edges[initial, i]
                remain.append(i)
        heuristic = MST(remain, edges)
        for v in remain:
            new_path = current.path.copy()
            new_path.append(v)
            q.put(Node(v, dist_from_init + current.path_cost + edges[current.state, v] + heuristic, new_path, current.path_cost + edges[current.state, v]))
    return Node(-1, 0, [-1], 0)

# for i in range(20):
#     vertices, edges = TSPGenerator(20)
#     # print(vertices)
#     # print(edges)

#     result1 = A_star(20, edges)
#     # result2 = A_star(20, edges)
#     print("result: ", result1.path_cost, result1.path)
