import numpy as np
import random
import TSP
import GA


def Hill_climbing(n, edges):
    current = list(range(n))
    random.shuffle(current)
    path_cost = GA.GetPathCost(current, edges)
    iteration = 0
    while True:
        best = 100000
        for i in range(0, n):
            for j in range(i + 1, n):
                tmp = current.copy()
                tmp[i], tmp[j] = tmp[j], tmp[i]
                new_cost = GA.GetPathCost(tmp, edges)
                if new_cost < best:
                    best = new_cost
                    best_state = tmp
        if best >= path_cost:
            break
        current = best_state
        path_cost = best
    # while True:
    #     iteration += 1
    #     # print(iteration, path_cost)
    #     next_state = current.copy()
    #     count = 0
    #     while True:
    #         count += 1
    #         if count > 1000000:
    #             return path_cost, current
    #         a = random.randint(0, n - 1)
    #         b = random.randint(0, n - 1)
    #         tmp = next_state[a]
    #         next_state[a] = next_state[b]
    #         next_state[b] = tmp
    #         new_cost = GA.GetPathCost(next_state, edges)
    #         if new_cost < path_cost:
    #             path_cost = new_cost
    #             current = next_state.copy()
    #             break
    return path_cost, current




count = 0
for i in range(100):
    vertices, edges = TSP.TSPGenerator(20)
    # hill climbing
    # path_cost, path = Hill_climbing(20, edges)
    # genetic algorithm
    path_cost, path = GA.GeneticAlgorithm(20, 300, 100, edges)
    # A* search
    result = TSP.A_star(20, edges)
    if path_cost - result.path_cost < 0.0000000001:
        count += 1

    print(path_cost, path)
    print(result.path_cost, result.path)
    print(count, '/', i)