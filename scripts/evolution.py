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
import pickle

from subprocess import call
import rospy
from ros_stdr_ga.srv import *


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
        rospy.wait_for_service('computeFitness')
        getFitnes = rospy.ServiceProxy('computeFitness', computeFitness)
        print "weights: " + str(cs)
        try:
            fit = getFitnes(cs)
        except rospy.ServiceException as exc:
            print("Service did not process request: " + str(exc))
            fit = 0
        print("fitness: " + str(fit))
        fitness.append(fit)
    return fitness


rand = Random()
rand.seed(int(time()))
# No idea
es = ec.ES(rand)
es.terminator = terminators.evaluation_termination

final_pop = es.evolve(generator=generate_phenotype,
                      evaluator=evaluate_population,
                      pop_size=10,
                      maximize=True,
                      max_evaluations=100,
                      mutation_rate=0.25,
                      num_inputs=9,
                      )
# Sort and print the best individual, who will be at index 0.
final_pop.sort(reverse=True)
print(final_pop[0])
pickle.dump(final_pop, open('/home/viki/final_pop', 'w'))
