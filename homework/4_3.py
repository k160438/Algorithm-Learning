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
        iteration += 1
        print(iteration, path_cost)
        next_state = current.copy()
        count = 0
        while True:
            count += 1
            if count > 1000000:
                return path_cost, current
            a = random.randint(0, n - 1)
            b = random.randint(0, n - 1)
            tmp = next_state[a]
            next_state[a] = next_state[b]
            next_state[b] = tmp
            new_cost = GA.GetPathCost(next_state, edges)
            if new_cost < path_cost:
                path_cost = new_cost
                current = next_state.copy()
                break
    return path_cost, current


vertices, edges = TSP.TSPGenerator(20)

# hill climbing
path_cost, path = Hill_climbing(20, edges)
# genetic algorithm
best_cost, best_path = GA.GeneticAlgorithm(20, 300, 100, edges)
# A* search
result = TSP.A_star(20, edges)

print(path_cost, path)
print(result.path_cost, result.path)