import numpy as np
import random
import TSP

def GetPathCost(path, edges):
    n = len(path)
    path_cost = edges[path[-1], path[0]]
    for i in range(n - 1):
        path_cost += edges[path[i], path[i + 1]]
    return path_cost

def selectBestIndiv(population, edges):
    best_cost = 100000
    best_path = []
    for i in range(len(population)):
        cost = GetPathCost(population[i], edges)
        if cost < best_cost:
            best_cost = cost
            best_path = population[i]
    return best_cost, best_path

# select parents
def selectParent(population, edges):
    p = len(population)
    fitness = np.zeros(p, dtype = float)
    for i in range(p):
        # fitness[i] = 1 / GetPathCost(population[i], edges)
        fitness[i] = GetPathCost(population[i], edges)
    fitness = np.max(fitness) - fitness
    sumOfFitness = np.sum(fitness)
    fitness = fitness / sumOfFitness

    for i in range(1, p):
        fitness[i] += fitness[i - 1]
    # print(fitness[50])
    new_population = []
    for i in range(int(p*0.95)):
        r = random.random()
        individual = 0
        while fitness[individual] < r:
            individual += 1
        # print(individual)
        new_population.append(population[individual])
    return new_population

# a method to crossover (order crossover referred to Larranaga's article)
def OX(indiv1, indiv2):
    n = len(indiv1)
    offspring1 = [-1]*n
    offspring2 = [-1]*n
    a = random.randint(0, n)
    b = random.randint(0, n)
    if b < a:
        a, b = b, a

    if a == b or b - a == n: 
        return indiv1, indiv2
    for i in range(a, b):
        offspring1[i] = indiv1[i]
        offspring2[i] = indiv2[i]
    pos_in_1 = b % n
    pos_in_2 = b % n
    for i in range(b, n + a):
        while indiv2[pos_in_2] in offspring1:
            pos_in_2 = (pos_in_2 + 1) % n
        offspring1[i % n] = indiv2[pos_in_2]
        while indiv1[pos_in_1] in offspring2:
            pos_in_1 = (pos_in_1 + 1) % n
        offspring2[i % n] = indiv1[pos_in_1]
    return offspring1, offspring2

# Genetic Algorithm
def GeneticAlgorithm(n, p, maxiter, edges):
    population = []
    individual = list(range(n))
    for i in range(p):
        random.shuffle(individual)
        randIndividual = individual.copy()
        population.append(randIndividual)

    for i in range(maxiter):
        best_cost, best_path = selectBestIndiv(population, edges)
        # print(i, best_cost, best_path)
        population = selectParent(population, edges)

        # reproduction with 5%
        for j in range(int(p * 0.05)):
            population.append(best_path) 
        random.shuffle(population)
        offspring = []
        for j in range(0, p, 2):
            
            # crossover
            offs1, offs2 = OX(population[j], population[j + 1])
            # print(np.sum(offs1))
            # mutation
            rand = random.random()
            if rand < 0.001:
                a = random.randint(0, n - 1)
                b = random.randint(0, n - 1)
                offs1[a], offs1[b] = offs1[b], offs1[a]
            rand = random.random()
            if rand < 0.001:
                a = random.randint(0, n - 1)
                b = random.randint(0, n - 1)
                offs2[a], offs2[b] = offs2[b], offs2[a]
            
            offspring.append(offs1)
            offspring.append(offs2)
        
        population = offspring

    best_cost, best_path = selectBestIndiv(population, edges)
    return best_cost, best_path

# for i in range(20):
#     vertices, edges = TSP.TSPGenerator(20)
#     result = TSP.A_star(20, edges)
#     best_cost, best_path = GeneticAlgorithm(20, 300, 100, edges)
#     print(i, '*'*20)
#     print("result:", best_cost, best_path)
#     print(result.path_cost, result.path)