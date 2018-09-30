import random
import numpy as np


# generate 8-puzzle problem that has solutions
def initialization():
    while True:
        puzzles = list(range(9))
        random.shuffle(puzzles)
        count = 0
        for i in range(9):
            for j in range(i + 1, 9):
                if puzzles[i] > puzzles[j]:
                    count += 1
        if count % 2 == 0:
            break 
    return puzzles

# compute the Manhattan distance of a state
def manhattan(puzzles):
    dist = 0
    pos = np.zeros((9, 2))
    for i in range(9):
        pos[puzzles[i]][0] = i % 3
        pos[puzzles[i]][1] = i // 3
    dist += abs(pos[1][0] - 1) + pos[1][1]
    dist += abs(pos[2][0] - 2) + pos[2][1]
    dist += pos[3][0] + abs(pos[3][1] - 1)
    dist += abs(pos[4][0] - 1) + abs(pos[4][1] - 1)
    dist += abs(pos[5][0] - 2) + abs(pos[5][1] - 1)
    dist += pos[6][0] + abs(pos[6][1] - 2)  
    dist += abs(pos[7][0] - 1) + abs(pos[7][1] - 2)
    dist += abs(pos[8][0] - 2) + abs(pos[8][1] - 2)
    return dist

# generate all successor state of current state
def successor_state(puzzles):
    def swap(puzzles, a, b):
        new = puzzles.copy()
        new[a], new[b] = new[b], new[a]
        return new
    
    result = []
    for i in range(9):
        if puzzles[i] == 0:
            zero_pos = i
            x = i % 3
            y = i //3
            break
    if x < 2:
        result.append(swap(puzzles, zero_pos, zero_pos + 1))
    if x > 0:
        result.append(swap(puzzles, zero_pos, zero_pos - 1))
    if y < 2:
        result.append(swap(puzzles, zero_pos, zero_pos + 3))
    if y > 0:
        result.append(swap(puzzles, zero_pos, zero_pos - 3))
    return result 


# first-choice hill climbing
def hill_climbing_first(puzzles):
    current = manhattan(puzzles)
    state = puzzles.copy()
    flag = True
    while flag:
        flag = False
        successors = successor_state(state)
        for next_state in successors:
            new_d = manhattan(next_state)
            if new_d < current:
                flag = True
                current = new_d
                state = next_state
                break
    return current, state

# steepest hill climbing
def hill_climbing_steepest(puzzles):
    current = manhattan(puzzles)
    state = puzzles.copy()
    flag = True
    while flag:
        flag = False
        successors = successor_state(state)
        for next_state in successors:
            new_d = manhattan(next_state)
            if new_d < current:
                flag = True
                current = new_d
                state = next_state
    return current, state

# hill climbing with random restart
def hill_climbing_restart(puzzles):
    dist = 10
    # state = []
    while dist > 0:
        dist, state = hill_climbing_steepest(puzzles)
        random.shuffle(puzzles)
    return dist, state

# simulated annealing algorithm
def simulated_annealing(puzzles):
    current = manhattan(puzzles)
    state = puzzles.copy()
    T = 10                 #initial temperature
    while True:
        if T < 0.0001: 
            break
        successors = successor_state(state)
        choice = np.random.randint(0, len(successors))
        next_state = successors[choice]
        new_d = manhattan(next_state)
        if new_d < current:
            current = new_d
            state = next_state.copy()
        else:
            r = random.random()
            if r < np.exp((current - new_d) / T):
                current = new_d
                state = next_state.copy()              
        T *= 0.999
    return current, state   


count = 0
for i in range(1000):
    puzzles = initialization()
    # print(manhattan(puzzles), puzzles)
    # dist, state = hill_climbing_first(puzzles)
    dist, state = hill_climbing_steepest(puzzles)
    # dist, state = hill_climbing_restart(puzzles)
    # dist, state = simulated_annealing(puzzles)
    if dist==0:
        count += 1
print(count, "/ 1000")

# puzzles = initialization()
# dist, state = hill_climbing_restart(puzzles)
# print(dist)