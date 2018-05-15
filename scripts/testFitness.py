#!/usr/bin/env python


# Usage: ./testFitness.py "[0.26541270855841015, 2.3723987998996523, 1.112445041333371, -3.6645262003373498, 3.254015651601733, -1.0413821751495358, 1.8689129328741996, -1.8586678260100264, 1.3335916372043641, -1.4594714079308095, 4.680444112809429, 4.488613746755305, -2.616023231834444, -7.309494053052205, 2.4629437509264624, -2.13079167098713, -2.098925995701339, 3.4348350789149227]"

import sys

from subprocess import call

if (len(sys.argv) == 1): 
	arg = str(range(18))
else:
	arg = sys.argv[1]
	#arg = "".join(arg).replace("[", "")
	#arg = "".join(arg).replace("]", "")

print("---")
print(arg)
print("---")

call(["rosservice", "call", "/computeFitness", arg])

