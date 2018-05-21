# -*- coding: utf-8 -*-
"""
Created on Tue May 15 20:07:37 2018
Evolution.py
@author: Juan
"""

from random import Random
from time import time
from inspyred import ec
from inspyred.ec import terminators

from subprocess import call




def generate_phenotype(random, args):
    size = args.get('num_inputs', 9)
    return [random.gauss(0, 1) for i in range(size)]



def evaluate_population(candidates, args):
    """
    My evaluation function
    
    :param: 
    """
    fitness = []
    for cs in candidates:
        try:
            arg = str(list(cs))
            output = call(["rosservice", "call", "/computeFitness", arg]) 
            fit = float(output.split(" ")[1])
            fitness.append(fit)
        except Exception as e:
            print(__file__)
            print(e)
#            return(0)
    return fitness


rand = Random()
rand.seed(int(time()))
# No idea
es = ec.ES(rand)
es.terminator = terminators.evaluation_termination

final_pop = es.evolve(generator=generate_phenotype,
                      evaluator=evaluate_population,
                      pop_size=100,
                      maximize=True,
                      max_evaluations=20,
                      mutation_rate=0.25,
                      num_inputs=9,
                      )
# Sort and print the best individual, who will be at index 0.
final_pop.sort(reverse=True)
print(final_pop[0])