import math
import random


def decode_value(value):
    return value >> 22, ( (1 << 22) -1 ) & value

def fitness(value):
    x, y = decode_value(value)
    t = x*x + y*y
    return 0.5 - (pow(math.sin(math.sqrt(t)), 2)- 0.5) / pow(1+0.001*t, 2)

def spin_roulette(cumulative_fitness):
    roulette = random.random() * cumulative_fitness[-1]
    for i, value in enumerate(cumulative_fitness):
        if value >= roulette: break
    return i

def generate_pair(cumulative_fitness):
    individual1 = spin_roulette(cumulative_fitness)
    individual2 = individual1

    while individual2 == individual1:
        individual2 = spin_roulette(cumulative_fitness)

    return (individual1, individual2) if individual1 < individual2 else (individual2, individual1)

def selection(population, fitness_function):
    best_individual = population[0]
    best_fitness = fitness_function(population[0])

    total = 0
    cumulative_fitness = []
    for individual in population:
        individual_fitness = fitness_function(individual)
        if individual_fitness > best_fitness:
            best_individual = individual
            best_fitness = individual_fitness

        total += individual_fitness
        cumulative_fitness.append(total)

    population_size = len(population)
    selected_pairs = []
    for _ in range(math.ceil(population_size/2)):
        pair = generate_pair(cumulative_fitness)
        while pair in selected_pairs:
            pair = generate_pair(cumulative_fitness)
        selected_pairs.append(pair)

    return selected_pairs, best_individual, best_fitness

def crossover(pair, n_bits,rate):
    if random.random() > rate:
        return pair

    cut = random.randint(1, n_bits-1)
    head_mask = (1 << cut) - 1
    mask = head_mask << (n_bits - cut)

    sun1 = (pair[0] & mask) | (pair[1] & ~mask)
    sun2 = (pair[1] & mask) | (pair[0] & ~mask)

    return sun1, sun2

def mutate(individual, n_bits,rate):
    if random.random() > rate:
        return individual

    position = random.randint(0, n_bits-1)
    return individual ^ (1 << position)

def genetic_algorithm(population, fitness_function, n_bits, crossover_rate = 0.80, mutation_rate = 0.1):
    best_individual, best_fitness = population[0], fitness_function(population[0])
    generations_without_improvement = 0
    while generations_without_improvement < 50:
        selected_pairs, best_selected_individual, best_selected_fitness = selection(population, fitness_function)

        if best_selected_fitness > best_fitness:
            best_individual = best_selected_individual
            best_fitness = best_selected_fitness
            generations_without_improvement = 0
        else:
            generations_without_improvement += 1

        next_generation = []
        for pair in selected_pairs:
            for individual in crossover(pair, n_bits, crossover_rate):
                mutated_individual = mutate(individual, n_bits, mutation_rate)
                next_generation.append(mutated_individual)

        population = next_generation

    return best_individual, best_fitness


population = [random.randint(-100,100) for _ in range(14)]
solution, value = genetic_algorithm(population, fitness, 44)
print(decode_value(solution), value)