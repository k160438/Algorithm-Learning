import math
import queue

def ACTIONS(vertex):
    all_state_set = GetAllState()  # return all the state space
    next_states = []
    for state in all_state_set:
        # check if vertex can reach this state next step
        if not IsCutOff(vertex, state):  
            next_states.append(state)
    return next_states


# the function to get distance between two points
def distance(a, b):
    return math.sqrt((a.x - b.x)**2+(a.y - b.y)**2)


# BFS search
def bfs():
    q = queue.Queue()
    q.put([S, 0])       # node consists of state and path cost
    while not q.empty():
        current = q.get()
        if current[0] == G:
            return Solution(current[1])
        next_states = ACTIONS(current[0])
        for state in next_states:
            if not IsInQueue(q, state):
                q.put([state, current[1] + distance(state, current[0])])
    return False


# ===================================================
# a datastructure to store state, f and g
class Node(object):
    # f: evaluation function     g: path cost
    def __init__(self, state, f, g):
        self.state = state
        self.f = f
        self.g = g
        return 

    def __lt__(self, other):
        return self.f < other.f

# A* search
def A_star():
    q = queue.PriorityQueue()
    q.put(Node(S, distance(S, G), 0))      
    while not q.empty():
        current = q.get()
        if current.state == G:
            return Solution(current.g)
        next_states = ACTIONS(current.state)
        path_cost = current.g
        for state in next_states:
            g = path_cost + distance(state, current.state)
            q.put(Node(state, g + distance(state, G), g))
    return False
