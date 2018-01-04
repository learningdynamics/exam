#! /usr/bin/python3

import unittest
import numpy as np

from graph import Graph
from ljal import LJAL

###
# temperature = 1000 * 0.97^play
# IL 
# Randomly generated CG out edge degrees: 2 and 3
# JAL


class LJALPart1(LJAL):

    def __init__(self, graph):
        super(LJALPart1, self).__init__(graph=graph, n_actions = 4)
        self.rewards = np.reshape(np.random.normal(0,50,self.n_actions**self.n_agents),
                                  [self.n_actions for i in range(self.n_agents)])

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
        super(LJAL2Part1, self).__init__(graph=graph)

        
class JALPart1(LJALPart1):

    def __init__(self):
        graph = FullGraph(5)
        super(JAL2Part1, self).__init__(graph=graph)
