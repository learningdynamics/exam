#! /usr/bin/python3

import unittest
import numpy as np

from graph import *

def BoltzmannAction(evs, temp=1):
    cs = np.cumsum(np.exp(np.array(evs)/temp))
    rd = np.random.uniform(0,cs[-1])
    return len(cs) - np.sum(rd <= cs)

def EVs(Q, N):
    return np.mean(Q, axis=0, weigths=N)

class LJAL(object):

    def __init__(self, graph, n_actions = 4):
        self.n_actions = n_actions
        self.graph = graph
        self.step = 0
        self.Qs = [ np.zeros((n_actions, n_actions**len(n))) for n in graph.nodes ]
        self.Ns = [ np.zeros((n_actions, n_actions**len(n)), dtype=np.int) for n in graph.nodes ]

    def one_step(self):
        actions = [ BoltzmannAction(EVs()) for agent in range(0, len(self.graph.nodes)) ]

        self.step += 1


####################
## TESTING
class TestLJALMethods(unittest.TestCase):

    def test_BoltzmannAction(self):
        self.assertTrue(BoltzmannAction([100,0,0]) == 0)
        self.assertTrue(BoltzmannAction([0,100,0,0]) == 1)
        self.assertTrue(BoltzmannAction([0,0,100,0,0]) == 2)
        self.assertTrue(BoltzmannAction([0,0,0,100]) == 3)
        half = np.mean([BoltzmannAction([10,10]) for i in range(0,2000)])
        self.assertTrue(0.45 < half and half < 0.55)

    def test_LJAL(self):
        g = Graph(5)
        g.add_arc(1,2)
        g.add_arc(1,3)
        l = LJAL(g)              
        self.assertTrue(np.shape(l.Qs[0]) == (4,1))
        self.assertTrue(np.shape(l.Qs[1]) == (4,4**2))
        self.assertTrue(np.shape(l.Ns[0]) == (4,1))
        self.assertTrue(np.shape(l.Ns[1]) == (4,4**2))

if __name__ == "__main__":
    unittest.main()
  
