#! /usr/bin/python3


from ljal import *
import sys
from timeit import default_timer as timer
from multiprocessing import Pool
import matplotlib.pyplot as plt
import tasks
import argparse
from dcop import DCOPpart2
import pickle

def actionsToEdges(actions, binary, n_agents=7):
    s = set()
    if binary:
        for i, a in enumerate(actions):
            a1 = a // n_agents
            a2 =  a % n_agents
            if (i != a1):
                s.add((i,a1))
            if (i != a2):
                s.add((i,a2))
    else:
        for i, a in enumerate(actions):
            if (i != a):
                s.add((i,a))
    return s


class LDCOPpart3(LJAL):
    
    def __init__(self, n_agents=7, binary=False, n_dcop = 100):
        self.n_agents = n_agents
        self.binary = binary
        self.n_dcop = n_dcop

        self.n_edges = n_agents**2 if binary else n_agents
        toplevel_IL_graph = Graph(n_agents)
        super(LDCOPpart3, self).__init__(graph=toplevel_IL_graph, n_actions=self.n_edges, optimistic=0.0)

    def _get_graph(self, actions):
        graph = Graph(self.n_agents)
        for i, a in actionsToEdges(actions, self.binary, self.n_agents):
            graph.add_arc(i,a)

        return graph

    def reward(self, actions):
        print(self.step)
        graph = self._get_graph(actions)
        def myDCOP(i):
            d = DCOPpart2(graph=graph)
            for n in range(200):
                d.one_step()
            return d.R

        res = np.mean(list(parmap(myDCOP, range(self.n_dcop))))

        return res

    def temperature(self):
        return 1000* 0.994 ** self.step

    def alpha(self):
        return 0.2

parser = argparse.ArgumentParser(description='Part 3.')
parser.add_argument('-ndcop', dest='n_dcop_samples', type=int, default=100,
                    help='number of samples for the internal DCOP (default: 100)')
parser.add_argument('-nsteps', dest='n_steps', type=int, default=1500,
                    help='number of steps (default: 1500)')
parser.add_argument('--save', dest='save_name', type=str, default="part3.pickle",
                    help='the filename of the plot (default: "part3.pickle")')

args = parser.parse_args()

print("Running optLJAL-1")
start = timer()
optLJAL1 = LDCOPpart3(n_dcop = args.n_dcop_samples)
optLJAL1_Rs = optLJAL1.n_steps(args.n_steps)
end = timer()
optLJAL1_time = end - start
print("Edges: {}".format(actionsToEdges(optLJAL1.actions, False)))

print("Running optLJAL-2")
start = timer()
optLJAL2 = LDCOPpart3(n_dcop = args.n_dcop_samples)
optLJAL2_Rs = optLJAL2.n_steps(args.n_steps)
end = timer()
optLJAL2_time = end - start
print("Edges: {}".format(actionsToEdges(optLJAL2.actions, True)))

todo = [{ "msg": "Running optLJAL-1", "name": "optLJAL-1", "fun":None, 
          "partners": 0, "n_samples": 1, "Rs": optLJAL1_Rs, "time": optLJAL1_time, "graph": optLJAL1.actions },
        { "msg": "Running optLJAL-2", "name": "optLJAL-2", "fun":None, 
          "partners": 0, "n_samples": 1, "Rs": optLJAL2_Rs, "time": optLJAL2_time, "graph": optLJAL2.actions }]

with open(args.save_name, 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(todo, f, pickle.HIGHEST_PROTOCOL)
