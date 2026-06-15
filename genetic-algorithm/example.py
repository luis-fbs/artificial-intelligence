import math
import random

from genetic_algorithm import genetic_algorithm


def bin_to_float(x):
    min, max, n_bits = -100, 100, 22
    distance = max - min
    step = distance / (2 ** n_bits - 1)
    return min + x * step

def decode_value(value):
    x_bin = value >> 22
    y_bin = ( (1 << 22) -1 ) & value
    x = bin_to_float(x_bin)
    y = bin_to_float(y_bin)
    return x, y

def fitness(value):
    x, y = decode_value(value)
    t = x*x + y*y
    return 0.5 - (pow(math.sin(math.sqrt(t)), 2)- 0.5) / pow(1+0.001*t, 2)

def seeder(population_size, n):
    seed = []
    for _ in range(n):
        population = [random.getrandbits(44) for _ in range(population_size)]
        i, f = genetic_algorithm(population, fitness, 44)
        seed.append(i)
    return seed


n = 500
population = seeder(100, n)
best_individual, best_fitness = genetic_algorithm(population, fitness, 44)
print(decode_value(best_individual), best_fitness)