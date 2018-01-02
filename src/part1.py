#! /usr/bin/python3

import unittest
import numpy as np
import matplotlib.pyplot as plt

from timeit import default_timer as timer
from multiprocessing import Pool
import sys

from graph import (Graph, RandomGraph, FullGraph)
from ljal import LJAL, AverageR

###
# temperature = 1000 * 0.97^play
# IL 
# Randomly generated CG out edge degrees: 2 and 3
# JAL

class Rewards(object):
    vec = np.random.normal(0,50,4**5)
    
    def __init__(self):
        pass

    def __len__(self):
        return len(Rewards.vec)

    def __getitem__(self, key):
        if isinstance( key, slice ) :
            return [self[ii] for ii in range(*key.indices(len(self)))]
        elif isinstance( key, int ):
            l = len(self)
            if key >= l:
                Rewards.vec.extend(np.random.normal(0,50,key-l+1+100))

        return Rewards.vec[key]


class LJALPart1(LJAL):

    def __init__(self, graph, alpha=0.1):
        super(LJALPart1, self).__init__(graph=graph, n_actions = 4, alpha = alpha)
        # Need global reward
        r = Rewards()
        self.rewards = np.reshape(r[0:self.n_actions**self.n_agents],
                                  [self.n_actions for i in range(0, self.n_agents)])

    def temperature(self):
        ## As described p. 5
        return 1000.0 * 0.94**self.step

    def reward(self, actions):
        return self.rewards[tuple(actions)]


n_samples = 10
if len(sys.argv) > 1:
    n_samples = int(sys.argv[1])

steps = 200
index = [i for i in range(1, steps+1)]

start = timer()
IL = AverageR(n_samples, lambda:LJALPart1(graph=Graph(5)).n_steps(steps))
end = timer()
IL_delta = end - start

start = timer()
LJAL_2 = AverageR(n_samples, lambda:LJALPart1(graph=RandomGraph(5, 2)).n_steps(steps))
end = timer()
LJAL_2_delta = end - start


start = timer()
LJAL_3 = AverageR(n_samples, lambda:LJALPart1(graph=RandomGraph(5, 3)).n_steps(steps))
end = timer()
LJAL_3_delta = end - start

start = timer()
JAL = AverageR(n_samples, lambda:LJALPart1(graph=FullGraph(5)).n_steps(steps))
end = timer()
JAL_delta = end - start


timing = np.array([IL_delta,  LJAL_2_delta, LJAL_3_delta, JAL_delta]) / JAL_delta
print( timing )


plt.ylim(-10, 120)
plt.plot(index, IL, 'r', index, LJAL_2, 'b', index, LJAL_3, 'g', index, JAL, 'y')
plt.ylabel('R')
plt.savefig('part1.png')
#plt.show()
