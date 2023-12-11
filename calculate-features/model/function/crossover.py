import random

def crossover(parent1, parent2): # Lai giua bo va me (1 phan cua bo, 1 phan cua me)
    crossover_point = random.randint(1, len(parent1) - 1)
    child = list(parent1[:crossover_point]) + list(parent2[crossover_point:])
    return tuple(child)

def two_point_crossover(parent1, parent2):
    crossover_point1, crossover_point2 = sorted(random.sample(range(1, len(parent1)), 2))
    child = list(parent1[:crossover_point1]) + list(parent2[crossover_point1:crossover_point2]) + list(parent1[crossover_point2:])
    return tuple(child)

def uniform_crossover(parent1, parent2, crossover_prob=0.5):
    child = [gene1 if random.random() < crossover_prob else gene2 for gene1, gene2 in zip(parent1, parent2)]
    return tuple(child)
