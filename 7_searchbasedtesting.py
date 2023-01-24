import random


def test_me(x, y):
    if x == 2 * (y + 1):
        return True
    else:
        return False


def get_fitness(test):
    return abs(test[0] - (2 * (test[1] + 1)))


num_parameters = 2
MAX = 1000000
MIN = -MAX


def get_random_test():
    return [random.randint(MIN, MAX) for _ in range(num_parameters)]


def get_neighbours(individual):
    neighbours = []

    for p in range(len(individual)):
        if individual[p] > MIN:
            neighbour = individual[:]
            neighbour[p] = individual[p] - 1
            neighbours.append(neighbour)

        if individual[p] < MAX:
            neighbour = individual[:]
            neighbour[p] = individual[p] + 1
            neighbours.append(neighbour)

    return neighbours


def hillclimbing():

    current = get_random_test()
    for i in range(10000):
        neighbours = get_neighbours(current)
        best_neighbour = min(neighbours, key=lambda x: get_fitness(x))
        if get_fitness(best_neighbour) < get_fitness(current):
            current = best_neighbour
        else:
            # Random restart
            current = get_random_test()

        print(f"Current fitness: {get_fitness(current)}")

    return current

test = hillclimbing()
print(test)
if test_me(*test):
    print("Target found")


def mutate(individual):
    P_mutate = 1/len(individual)
    mutated = individual[:]
    for position in range(len(individual)):
        if random.random() < P_mutate:
            mutated[position] = int(random.gauss(mutated[position], 20))

    return mutated


def crossover(parent1, parent2):
    pos = random.randint(0, len(parent1))
    offspring1 = parent1[:pos] + parent2[pos:]
    offspring2 = parent2[:pos] + parent1[pos:]

    return offspring1, offspring2


tournament_size = 3
def selection(population):
    candidates = random.sample(population, tournament_size)
    winner = min(candidates, key=lambda x: get_fitness(x))
    return winner


elite_size = 2
def elitism(population):
    population.sort(key = lambda x: get_fitness(x))
    return population[:elite_size]

population_size = 30
max_gen = 100
P_xover = 0.7

def ga():
    population = [get_random_test() for _ in range(population_size)]
    best_individual = min(population, key = lambda x: get_fitness(x))
    best_fitness = get_fitness(best_individual)

    for i in range(max_gen):
        new_population = elitism(population)
        while len(new_population) < len(population):
            parent1 = selection(population)
            parent2 = selection(population)

            if random.random() < P_xover:
                offspring1, offspring2 = crossover(parent1, parent2)
            else:
                offspring1, offspring2 = parent1, parent2

            offspring1 = mutate(offspring1)
            offspring2 = mutate(offspring2)

            new_population.append(offspring1)
            new_population.append(offspring2)

        population = new_population
        best_individual = min(population, key=lambda x: get_fitness(x))
        best_fitness = get_fitness(best_individual)
        print(f"Generation {i}: Fitness {best_fitness}")

    return best_individual

print(ga())