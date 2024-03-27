__copyright__ = """
武満世阿弥
TAKEMITSU, Zeami [birth name]
("Willard-Southward, Brien")
"""

__outside_sources__ = """
https://github.com/kiecodes/genetic-algorithms/
https://www.youtube.com/watch?v=nhT56blfRpE
"""

import random
import numpy as np
from typing import List, Optional, Callable, Tuple

#import action_classes # class definitions for wizards and game actions

Genome = List[int]
Population = List[Genome]
PopulateFunc = Callable[[], Population]
FitnessFunc = Callable[[Genome], int]
SelectionFunc = Callable[[Population, FitnessFunc], Tuple[Genome, Genome]]
CrossoverFunc = Callable[[Genome, Genome], Tuple[Genome, Genome]]
MutationFunc = Callable[[Genome], Genome]
PrinterFunc = Callable[[Population, int, FitnessFunc], None]

# For re-implementation using unit vector floats
GenomeF = List[float]
PopulationF = List[GenomeF]
PopulateFuncF = Callable[[], PopulationF]
FitnessFuncF = Callable[[GenomeF], float]
SelectionFuncF = Callable[[PopulationF, FitnessFuncF], Tuple[GenomeF, GenomeF]]
CrossoverFuncF = Callable[[GenomeF, GenomeF], Tuple[GenomeF, GenomeF]]
MutationFuncF = Callable[[GenomeF], GenomeF]
PrinterFuncF = Callable[[Population, int, FitnessFuncF], None]

def generate_genome(length: int) -> Genome:
    """
    The genome is represented as an array of integers in the original implementation.
    This could be replaced by an array of floats in the unit vector.
    """
    return random.choices([0,1], k=length) 


def generate_population(size: int, genome_length: int) -> Population:
    return [generate_genome(genome_length) for _ in range(size)]


def single_point_crossover(a: Genome, b: Genome) -> Tuple[Genome, Genome]:
    """
    This takes in two genomes, splits them at one point, and crosses them over.
    """
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of the same length.")
    
    length = len(a)
    if length < 2:
        return a, b
    
    p = random.randint(1, length - 1)
    return a[0:p] + b[p:], b[0:p] + a[p:]


def mutation(genome: Genome, num: int = 1, probability: float = 0.5) -> Genome:
    """
    Args: Genome to mutate, number of attempted mutation sites, probability of mutation
    """
    for _ in range(num):
        index = random.randrange(len(genome))
        genome[index] = genome[index] if random.random() > probability else abs(genome[index] - 1) # abs(genome[index] - 1) is just a bit flip here...
    return genome


def population_fitness(population: Population, fitness_func: FitnessFunc) -> int:
    """Fitness of the entire population."""
    return sum([fitness_func(genome) for genome in population])


def selection_pair(population: Population, fitness_func: FitnessFunc) -> Population:
    """Random weighted choice of 2 elements of Population based on weights assessed by fitness function.
    The way the main fitness function is defined sets the weight to 0 for a sum below a threshold (see below)."""
    return random.choices(population=population, 
                          weights=[fitness_func(genes) for genes in population],
                          k=2)


def fitness(genome: Genome, threshold: int) -> int:
    """Assigns fitness of 0 if the genome's sum is below a threshold."""
    value = sum(genome) # sum up the 1s and 0s
    if value < threshold:
        return 0
    else:
        return value
  
        
def sort_population(population: Population, fitness_func: FitnessFunc) -> Population:
    return sorted(population, key=fitness_func, reverse=True)


def run_evolution(populate_func: PopulateFunc,
        fitness_func: FitnessFunc,
        fitness_limit: int,
        selection_func: SelectionFunc = selection_pair,
        crossover_func: CrossoverFunc = single_point_crossover,
        mutation_func: MutationFunc = mutation,
        generation_limit: int = 100) -> Tuple[Population, int]:
    population = populate_func()
    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)
        
        if fitness_func(population[0]) >= fitness_limit:
            break
        
        next_generation = population[0:2]
        
        for j in range(int(len(population)/2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]
            
        population = next_generation
        
    return population, i





"""Experimental Section"""
def generate_genome_f(length: int) -> GenomeF:
    """
    The genome is represented as an array of integers in the original implementation.
    Here it's floats that average out instead of doing a single-point crossover.
    """
    return [random.random() for _ in range(length)] # floats in [0., 1.]


def generate_population_f(size: int, genome_length: int) -> PopulationF:
    return [generate_genome_f(genome_length) for _ in range(size)]


def crossover_and_avg_f(a: GenomeF, b: GenomeF) -> Tuple[GenomeF, GenomeF]:
    """
    This also takes in two genomes, splits them at one point, and crosses them over.
    But since it's floats in the unit vector, let's do something like average and reverse.
    """
    if len(a) != len(b):
        raise ValueError("Genomes a and b must be of the same length.")
    
    length = len(a)
    if length < 2:
        return a, b
    
    avg = [(i+j)*0.5 for i,j in zip(a,b)]
    avg_r = avg[::-1] # reverse using list slicing
    a = avg
    b = avg_r
    
    p = random.randint(1, length - 1) # random crossover point 
    aa, bb = a[0:p] + b[p:], b[0:p] + a[p:]
    return aa, bb


def mutation_f(genome: GenomeF, num: int = 1, probability: float = 0.5) -> GenomeF:
    """
    Args: Genome to mutate, number of attempted mutation sites, probability of mutation
    """
    for _ in range(num):
        index = random.randrange(len(genome))
        genome[index] = genome[index] if random.random() > probability else abs(genome[index] - 1) # ... but abs(genome[index] - 1) is 1's complement here
    return genome


def population_fitness_f(population: PopulationF, fitness_func_f: FitnessFuncF) -> float:
    """Fitness of the entire population in Float realm."""
    return sum([fitness_func_f(genome) for genome in population])


def selection_pair_f(population: PopulationF, fitness_func_f: FitnessFuncF) -> PopulationF:
    """Random weighted choice of 2 elements of Population based on weights assessed by fitness function.
    The way the main fitness function is defined sets the weight to 0 for a sum below a threshold (see below)."""
    return random.choices(population=population, 
                          weights=[fitness_func_f(genes) for genes in population],
                          k=2)


def fitness_f(genome: Genome, threshold: float) -> float:
    """Assigns fitness of 0 if the genome's sum is below a threshold."""
    value = sum(genome) # sum up the floats in unit vector [0., 1.]
    if value < threshold:
        return 0.0
    else:
        return value
    

def sort_population_f(population: PopulationF, fitness_func: FitnessFunc) -> PopulationF:
    return sorted(population, key=fitness_func, reverse=True)    


def run_evolution_f(populate_func: PopulateFuncF,
        fitness_func: FitnessFuncF,
        fitness_limit: int,
        selection_func: SelectionFuncF = selection_pair_f,
        crossover_func: CrossoverFuncF = crossover_and_avg_f,
        mutation_func: MutationFuncF = mutation_f,
        generation_limit: int = 100) -> Tuple[PopulationF, int]:
    population = populate_func()
    for i in range(generation_limit):
        population = sorted(population, key=lambda genome: fitness_func(genome), reverse=True)
        
        if fitness_func(population[0]) >= fitness_limit:
            break
        
        next_generation = population[0:2]
        
        for j in range(int(len(population)/2) - 1):
            parents = selection_func(population, fitness_func)
            offspring_a, offspring_b = crossover_func(parents[0], parents[1])
            offspring_a = mutation_func(offspring_a)
            offspring_b = mutation_func(offspring_b)
            next_generation += [offspring_a, offspring_b]
            
        population = next_generation
        
    return population, i





def test_genome():
    a = generate_genome(10)
    b = generate_genome(10)
    crossover = single_point_crossover(a,b)
    print(a,b)
    print(crossover)
    return a, b

#test_genome()

def test_genome_f():
    testpop = generate_population_f(10, 10)
    mutated = [mutation_f(p, 3, 0.5) for p in testpop]
    print("Test population: \n", testpop, "\n\nMutated population: \n", mutated)
    return testpop, mutated
    
#test_genome_f()
    
#print(generate_genome_f(10))
#print(generate_population_f(2, 10))
#testpop = generate_population_f(10, 10)
#mutated = [mutation_f(p, 3, 0.5) for p in testpop]
#print("Test population: \n", testpop, "\n\nMutated population: \n", mutated)