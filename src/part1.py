#! /usr/bin/python3

import unittest
import numpy as np

from graph import Graph
from ljal import LJAL


class LJALPart1(LJAL):

    def __init__(self, graph):
        super(LJALPart1, self).__init__(graph=graph, n_actions = 4)
        # self.rewards = np.

    def temperature(self):
        ## As described p. 5
        return 1000 * 0.94**self.step

    def reward(self, actions):
        # use self.reward[actions]
        return 1

    

class ILPart1(LJALPart1):

    def __init__(self):
        graph = Graph(5)
        super(ILPart1, self).__init__(graph=graph)

        
class LJAL2Part1(LJALPart1):

    def __init__(self):
        graph = Graph(5)
        for n in range(0,5):
            graph.add(n, numpy.random.randint(0, 5))
        super(LJAL2Part1, self).__init__(graph=graph)
