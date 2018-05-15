# -*- coding: utf-8 -*-
"""
Created on Tue May 15 20:07:37 2018
Evolution.py
@author: Juan
"""

from pybrain.tools.shortcuts import buildNetwork
from pybrain.structure.modules.sigmoidlayer import SigmoidLayer

ann = buildNetwork(4,1,2, hiddenclass=SigmoidLayer)