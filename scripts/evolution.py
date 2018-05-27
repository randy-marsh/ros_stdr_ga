# -*- coding: utf-8 -*-
"""
Created on Tue May 15 20:07:37 2018
Evolution.py
@author: Juan
"""

from random import Random
from time import time
import inspyred
from inspyred import ec
from inspyred.ec import terminators, variators
import pickle

from subprocess import call
import rospy
from ros_stdr_ga.srv import *


def generate_phenotype(random, args):
    size = args.get('num_inputs', 30)
    return [random.gauss(0, 0.5) for i in range(size)]



def evaluate_population(candidates, args):
    """
    My evaluation function
    
    :param: 
    """
    fitness = []
    for cs in candidates:
        rospy.wait_for_service('computeFitness')
        getFitnes = rospy.ServiceProxy('computeFitness', computeFitness)
#        print "weights: " + str(cs)
        try:
            fit = getFitnes(cs)
        except rospy.ServiceException as exc:
            print("Service did not process request: " + str(exc))
            fit = 0
        print("fitness: " + str(fit))
        fitness.append(fit)
    return fitness
# from https://gist.github.com/dfbarrero/70138ef2b76c51dade887eb4f7f06fa8
#def showStatistics(population, num_generations, num_evaluations, args):
#    stats = inspyred.ec.analysis.fitness_statistics(population)
#    print('Generation {0}, best fit {1}, avg. fit {2}'.format(num_generations,
#          stats['best'], stats['mean']))


if __name__ == '__main__':
    
    rand = Random()
    rand.seed(int(time()))
    # No idea
    #es = ec.ES(rand)
    ga = ec.GA(rand)
#    dea = ec.DEA(rand)
    #ga.evolve()
    #es.terminator = terminators.evaluation_termination
#    dea.terminator = terminators.generation_termination
#    dea.variator = variators.arithmetic_crossover
    ga.terminator = terminators.generation_termination
    ga.variator = variators.arithmetic_crossover
#    ga.observer = showStatistics
    
    final_pop = ga.evolve(generator=generate_phenotype,
                          evaluator=evaluate_population,
                          pop_size=5,
                          max_generations=3,
#                          num_selected=0,
                          maximize=True,
#                          max_evaluations=50,
#                          crossover_rate=0.9,
                          mutation_rate=0.4,
                          num_inputs=30,
                          num_elites=1
#                          gaussianstdev=0.5
                          )
    # Sort and print the best individual, who will be at index 0.
    best = max(final_pop)
    print('Best Solution: \n{0}'.format(str(best)))
#    final_pop.sort(reverse=True)
#    print(final_pop[0])
    pickle.dump(final_pop, open('/home/viki/final_pop', 'w'))
