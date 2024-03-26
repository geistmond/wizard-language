__copyright__ = """
武満世阿弥
TAKEMITSU, Zeami
("Willard-Southward, Brien")
"""

__use__ = """
Ultimately this is part of a game design that is a multi-agent system.
Game events are encoded using a fully-specified language that also serves as the spell-casting language.
Loss functions and optimization methods are intended to speed up the agents' decision-making at population scale.
"""

__outsidecredit__ = """
Based on this example and other YouTube evolutionary algorihtms algorithms:
https://www.youtube.com/watch?v=4XZoVQOt-0I

This generates random possible solutions to a polynomial, checks them, randomizes, checks again.
It approximates the result already in the polynomial, i.e. if you apply Cartesian multiplication a zero is always at n.
"""

import random
import numpy as np

from matplotlib import pyplot
from mpl_toolkits.mplot3d import Axes3D

from typing import Callable

from functools import lru_cache

def simple_example()->None:
    # Cartesian multiplication for a polynomial's solutions
    def polynomial(x: float,y: float,z: float,coef: tuple[float])->float:
        i, j, k, n = coef[0], coef[1], coef[2], coef[3]
        ans = i*x**3 + j*y**2 + k*z - n
        
        if ans == 0:
            return 1e+128
        else:
            return abs(1.0/ans)
        
    # Default coefficients
    coef = (6., 9., 90., 25.)


    # Space of random candidate solutions
    solutions = []
    for s in range(1000):
        solutions.append((random.uniform(0,10000), 
                        random.uniform(0,10000), 
                        random.uniform(0,10000)))

    # Selection Phase
    for i in range(10000):
        ranked_solutions = []
        for s in solutions:
            ranked_solutions.append(((polynomial(s[0],s[1],s[2],coef), s)))
        ranked_solutions.sort()
        ranked_solutions.reverse()
        
        print(f"=== Gen{i} best solutions ===")
        print(ranked_solutions[0])
        
        if ranked_solutions[0][0] > 999:
            break
        
        best_solutions = ranked_solutions[:100]
        
        elements = []
        for s in best_solutions:
            elements.append(s[1][0])
            elements.append(s[1][1])
            elements.append(s[1][2])
            
        # Mutation Phase
        new_gen = []
        for _ in range(1000):
            e1 = random.choice(elements) * random.uniform(0.99, 1.01)
            e2 = random.choice(elements) * random.uniform(0.99, 1.01)
            e3 = random.choice(elements) * random.uniform(0.99, 1.01)
            new_gen.append((e1,e2,e3))

        solutions = new_gen
    print("Done.")
    return None
    
    

# Additional evolutionary algorithm example, the Ackley function optimizer
def ackley_result(x: float, y: float)->float:
    return -20.0 * np.exp(-0.2 * np.sqrt(0.5 * (x**2. + y**2.))) - np.exp(0.5 * (np.cos(2. * np.pi * x) + np.cos(2. * np.pi * y))) + np.e + 20.


# try things
def ackley_new(x: float, y: float, z: float)->float:
    """Adds a Z term with tangent function in place of scalar."""
    return np.tan(-2. * np.pi * z) * np.exp(-0.2 * np.sqrt(0.5 * (x**2. + y**2.))) - np.exp(0.5 * (np.cos(2. * np.pi * x) + np.cos(2. * np.pi * y))) + np.e + np.tan(2. * np.pi * z)

# boolean result about a function being in bounds
@lru_cache
def in_bounds(points: list[float], bounds: list[float])->bool:
    for d in range(len(bounds)):
        if points[d] < bounds[d, 0] or points[d] > bounds[d, 1]:
            return False
        return True
    
# some other examples of boolean constraints
@lru_cache
def should_buy(n: float, threshold: float)->bool:
    if n < threshold:
        print("buy")
        return True
    return False

@lru_cache
def should_sell(n: float, threshold: float)->bool:
    if n > threshold:
        print("sell")
        return True
    return False

@lru_cache
def buy_or_sell(n: float, bounds: list[float])->str:
    minimum = list[0]
    maximum = list[1]
    if should_buy(n, minimum):
        return "buy"
    elif should_sell(n, maximum):
        return "sell"
    

# Competition function Es Comma
#@lru_cache #memoizer
def es_comma(objective: Callable[[float,float], float], 
             bounds: list[float], 
             n_iter: int, 
             step_size: float, 
             mu: int, 
             lam: int) -> list[list[float]]:
    """Es Comma algorithm is a graph search reducer for optimizing possible zeroes."""
    best, best_eval = None, 1e+10
    # calcualte children per parent
    n_children = int(lam/mu)
    # initial population
    population = np.ndarray()
    for _ in range(lam):
        candidate = None
        while candidate is None or not in_bounds(candidate, bounds):
            candidate = bounds[:,0] + np.rand(len(bounds)) * (bounds[:,1] - bounds[:,0])
        population.append(candidate)
    # perform the search
    for epoch in range(n_iter):
        # evaluate fitness for population
        scores = [objective(c) for c in population]
        # rank scores in ascending order
        ranks = np.argsort(np.argsort(scores))
        # select the indices for the top mu ranked solutions
        selected = [i for i,_ in enumerate(ranks) if ranks[i] < mu]
        # create children from parents
        children = np.ndarray()
        for i in selected:
            if scores[i] < best_eval:
                best, best_eval = population[i], scores[i]
                print('%d, Best: f(%s) = %.5f' % (epoch, best, best_eval))
            # create children for parent
            for _ in range(n_children):
                child = None
                while child is None or not in_bounds(child, bounds):
                    child = population[i] + np.random.randn(len(bounds)) * step_size
                children.append(child)
            # replace population with children
            population = children
    return [best, best_eval]
        
 
 
def plot_function(r_min, r_max)->None:
    x_axis = np.arange(r_min, r_max, 0.1)
    y_axis = np.arange(r_min, r_max, 0.1)
    x, y = np.meshgrid(x_axis, y_axis)
    results = ackley_result(x, y)
    figure = pyplot.figure()
    axis = figure.add_subplot(projection='3d')
    axis.plot_surface(x, y, results, cmap='jet')
    pyplot.show()
    return None

plot_function(-10, 10)