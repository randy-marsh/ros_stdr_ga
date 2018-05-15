# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 20:23:10 2018

@author: Juan
"""

import numpy as np

class MLPException(Exception):
    pass

def create(vin, topology):
    """
    """

    layers = {}
    inputlen = [vin] + list(topology)
    for i in range(len(inputlen) -1):
        layers['l' + str(i)] = np.random.random((inputlen[i], inputlen[i + 1]))
#        l1 = np.zeros((vin, topology[0]), dtype=np.float32)
    return layers

def size(layers):
    size = 0
    for key, value in layers.iteritems():
        size +=value.size
    return size

def fit(wvector, layers):
    """
    """
    lsize = size(layers)
    # sanity check
    if wvector.shape[0] != lsize:
        raise MLPException('wvector and weight size dont match')
    
