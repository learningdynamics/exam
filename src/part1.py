import unittest
import numpy as np
import matplotlib.pyplot as plt
import argparse

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
    vec = np.random.normal(0, 50, 4 ** 5)

    def __init__(self):
        pass

    def __len__(self):
        return len(Rewards.vec)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return [self[ii] for ii in range(*key.indices(len(self)))]
        elif isinstance(key, int):
            l = len(self)
            if key >= l:
                Rewards.vec.extend(np.random.normal(0, 50, key - l + 1 + 100))

        return Rewards.vec[key]


class LJALPart1(LJAL):
    def __init__(self, graph):
        super(LJALPart1, self).__init__(graph=graph, n_actions=4, optimistic=0.0)
        # Need global reward
        r = Rewards()
        self.rewards = np.reshape(r[0:self.n_actions ** self.n_agents],
                                  [self.n_actions for i in range(0, self.n_agents)])

    def alpha(self):
        # return 1/np.log2(self.step+2)
        return 0.8

    def temperature(self):
        ## As described p. 5
        return 1000.0 * 0.94 ** self.step

    def reward(self, actions):
        return self.rewards[tuple(actions)]



parser = argparse.ArgumentParser(description='Part 1.')
parser.add_argument('-n', dest='n_samples', type=int, default=100,
                    help='number of samples (default: 100)')
parser.add_argument('--plot', dest='plot_name', type=str, default="part1_plot.png",
                    help='the filename of the plot (default: "part1_plot.png")')
parser.add_argument('--latex', dest='table_name', type=str, default="part1_table.tex",
                    help='the filename of the LaTeX table (default: "part1_table.tex")')

args = parser.parse_args()
    
steps = 200

full_graph = FullGraph(5)
todo = [{ "msg": "Running IL", "name": "IL", "partners": 0,
          "fun":lambda: LJALPart1(graph=Graph(5)).n_steps(steps)},
        { "msg": "Running LJAL-2", "name": "LJAL-2", "partners": 2,
          "fun": lambda: LJALPart1(graph=RandomGraph(5, 2)).n_steps(steps)},
        { "msg":"Running LJAL-3", "name": "LJAL-3", "partners": 3,
          "fun": lambda: LJALPart1(graph=RandomGraph(5, 3)).n_steps(steps)},
        { "msg":"Running JAL", "name":"JAL", "partners": 4,
          "fun": lambda: LJALPart1(graph=full_graph).n_steps(steps)}]

for t in todo:
    print(t["msg"])
    start = timer()
    t["Rs"] = AverageR(args.n_samples, t["fun"])
    end = timer()
    t["time"] = end - start


print("Plotting")
index = [i for i in range(1, steps + 1)]
plt.ylim(-10, 120)
for t in todo:
    plt.plot(index, t["Rs"])
plt.legend([t["name"] for t in todo])
plt.ylabel('R')
plt.savefig(args.plot_name)
# plt.show()


row_format ="{:>10} & {:>15} & {:>15} & {:>16} \\\\\n"
with open(args.table_name, 'w') as f:
    f.write('\\begin{tabular}{lllr}\n')
    f.write('\\toprule\n')
    f.write(row_format.format("Learner", "Avg # Partners", "Speed", "Solution Quality"))
    f.write('\\midrule\n')
    for t in todo:
        f.write( row_format.format(t["name"],
                                   "${}$".format(t["partners"]),
                                   "$\\times {:.1f}$".format(todo[-1]["time"] / t["time"]),
                                   "${:.1f}$\\%".format(t["Rs"][-1]/todo[-1]["Rs"][-1] * 100) ) )
    f.write('\\bottomrule\n')
    f.write("\\end{tabular}\n")
