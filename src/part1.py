#! /usr/bin/python3

import unittest
import numpy as np
import matplotlib.pyplot as plt

from graph import (Graph, RandomGraph, FullGraph)
from ljal import LJAL, AverageR

###
# temperature = 1000 * 0.97^play
# IL 
# Randomly generated CG out edge degrees: 2 and 3
# JAL


class LJALPart1(LJAL):

    def __init__(self, graph):
        super(LJALPart1, self).__init__(graph=graph, n_actions = 4)
        self.rewards = np.reshape(np.random.normal(0,50,self.n_actions**self.n_agents),
                                  [self.n_actions for i in range(0, self.n_agents)])

    def temperature(self):
        ## As described p. 5
        return 1000 * 0.94**self.step

    def reward(self, actions):
        return self.rewards[tuple(actions)]

        
class LJALNPart1(LJALPart1):

    def __init__(self, n_out = 0):
        """
        n_out: number of out edges. 
               n_out: 0 is IL 
                    : 2 is LJAL-2
                    : 3 is LJAL-3

        """
        graph = RandomGraph(5, n_out)
        super(LJALNPart1, self).__init__(graph=graph)

        
class JALPart1(LJALPart1):

    def __init__(self):
        graph = FullGraph(5)
        super(JALPart1, self).__init__(graph=graph)


steps = 200
index = [i for i in range(1, steps+1)]
IL = AverageR(20, lambda:LJALNPart1().n_steps(steps))
LJAL_2 = AverageR(20, lambda:LJALNPart1(n_out = 2).n_steps(steps))
LJAL_3 = AverageR(20, lambda:LJALNPart1(n_out = 3).n_steps(steps))
JAL = AverageR(20, lambda:JALPart1().n_steps(steps))

print(len(index))
print(len(IL))
print(len(LJAL_2))
print(len(LJAL_3))
print(len(JAL))

plt.plot(index, IL, 'r', index, LJAL_2, 'b', index, LJAL_3, 'g', index, JAL, 'y')
plt.ylabel('R')
plt.show()
