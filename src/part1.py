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
        # self.rewards = np.

    def temperature(self):
        ## As described p. 5
        return 1000 * 0.94**self.step

    def reward(self, actions):
        # use self.rewards[actions]
        return 1

        
class LJALNPart1(LJALPart1):

    def __init__(self, n_out = 0):
        """
        n_out: number of out edges. n_out = 0 is IL. n_out = 3 is LJAL-3
        """
        graph = Graph(5)
        for n in range(0,5):
            for i in range(0, n_out):
                graph.add_arc(n, numpy.random.randint(0, 5))
        super(LJAL2Part1, self).__init__(graph=graph)

class JALPart1(LJALPart1):

    def __init__(self):
        graph = Graph(5)
        for n1 in range(0,5):
            for n2 in range(0,5):
                if n1 != n2:
                    graph.add_arc(n1, n2)
        super(JAL2Part1, self).__init__(graph=graph)
