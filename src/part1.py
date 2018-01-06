import unittest
import numpy as np
import argparse
import pickle

from timeit import default_timer as timer
from multiprocessing import Pool
import sys

from graph import (Graph, RandomGraph, FullGraph)
from ljal import LJAL, AverageR
import tasks

###
# temperature = 1000 * 0.97^play
# IL 
# Randomly generated CG out edge degrees: 2 and 3
# JAL


class LJALPart1(LJAL):
    def __init__(self, graph):
        super(LJALPart1, self).__init__(graph=graph, n_actions=4, optimistic=0.0)
        self.rewards = np.reshape(np.random.normal(0, 50, self.n_actions ** self.n_agents),
                                  [self.n_actions for i in range(0, self.n_agents)])

    def alpha(self):
        # return 1/np.log2(self.step+2)
        return 0.5

    def temperature(self):
        ## As described p. 5
        return 1000.0 * 0.94 ** self.step

    def reward(self, actions):
        return self.rewards[tuple(actions)]



parser = argparse.ArgumentParser(description='Part 1.')
parser.add_argument('-n', dest='n_samples', type=int, default=100,
                    help='number of samples (default: 100)')
parser.add_argument('--save', dest='save_name', type=str, default="part1.pickle",
                    help='the filename of the plot (default: "part1.pickle")')

args = parser.parse_args()
    
steps = 200

full_graph = FullGraph(5)
todo = [{ "msg": "Running IL", "name": "IL", "partners": 0, "n_samples": args.n_samples,
          "fun":lambda: LJALPart1(graph=Graph(5)).n_steps(steps)},
        { "msg": "Running LJAL-2", "name": "LJAL-2", "partners": 2, "n_samples": args.n_samples,
          "fun": lambda: LJALPart1(graph=RandomGraph(5, 2)).n_steps(steps)},
        { "msg":"Running LJAL-3", "name": "LJAL-3", "partners": 3, "n_samples": args.n_samples,
          "fun": lambda: LJALPart1(graph=RandomGraph(5, 3)).n_steps(steps)},
        { "msg":"Running JAL", "name":"JAL", "partners": 4, "n_samples": args.n_samples,
          "fun": lambda: LJALPart1(graph=full_graph).n_steps(steps)}]

tasks.run(todo, args.save_name)
