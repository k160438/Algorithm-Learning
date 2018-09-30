import random
import numpy as np


# the queens have no contradiction at crossing because 
# I use a sequence (0 - 7) to represent the position of queens
def initialization():
    queens = list(range(8))
    random.shuffle(queens)
    return queens

# only need to consider about the contradiction on the diagon
def collision(queens):
    res = 0
    for i in range(8):
        for j in range(i + 1, 8):
            if abs(i - j) == abs(queens[i] - queens[j]):
                res += 1
    return res


# two search strategies, mode 0 represents first-choice, mode 1 represents steepest-ascent
def hill_climbing(queens, mode = 0):
    flag = True
    current = collision(queens)
    state = queens.copy()
    while flag:
        flag = False
        best = 10000
        F = False
        for i in range(8):
            if F: break
            for j in range(i + 1, 8):
                candidate_state = state.copy()
                candidate_state[i], candidate_state[j] = candidate_state[j], candidate_state[i]
                new_h = collision(candidate_state)
                if new_h < current:
                    flag = True
                    if mode == 0:
                        state = candidate_state
                        current = new_h
                        F = True
                        break
                    else:
                        if new_h < best:
                            best = new_h
                            best_state = candidate_state
        if mode and flag:
            state = best_state
            current = best
    return current, state


# hill climbing with random restart
def hill_climbing_restart(queens):
    pairs, pos = hill_climbing(queens, 1)
    while pairs > 0:
        queens = initialization()
        pairs, pos = hill_climbing(queens, 1)
    return pairs, pos


# this is an algorithm that searches randomly, but it can reach almost all optimal solutions
def mysterious(queens):
    current = collision(queens)
    state = queens.copy()
    for i in range(1000):
        if current == 0:
            break
        a = random.randint(0, 7)
        b = random.randint(0, 7)
        while a == b:
            b = random.randint(0, 7)
        # print(a, b)
        tmp = state.copy()
        tmp[a], tmp[b] = tmp[b], tmp[a]
        new_h = collision(tmp)
        # print(new_h)
        if new_h <= current:     
            # if there is not equality, then the correct rate is only 0.3 ~ 0.4
            current = new_h
            state = tmp
    return current, state


# simulated annealing algorithm
def simulated_annealing(queens):
    current = collision(queens)
    state = queens.copy()
    T = 5                 #initial temperature
    while True:
        if T < 0.001: 
            break
        a = random.randint(0, 7)
        b = random.randint(0, 7)
        while a == b:
            b = random.randint(0, 7)
        # print(a, b)
        tmp = state.copy()
        tmp[a], tmp[b] = tmp[b], tmp[a]
        new_h = collision(tmp)
        if new_h < current:
            current = new_h
            state = tmp
        else:
            r = random.random()
            if r < np.exp((current - new_h) / T):
                current = new_h
                state = tmp                
        T *= 0.99
    return current, state


count = 0
for i in range(1000):
    queens = initialization()
    pairs, pos = hill_climbing(queens, 0)
    # pairs, pos = mysterious(queens)
    # pairs, pos = hill_climbing_restart(queens)
    # pairs, pos = simulated_annealing(queens)
    if pairs == 0:
        count += 1
print(count, '/ 1000')

# queens = initialization()
# pairs, pos = hill_climbing_restart(queens)
# print(pairs, pos)