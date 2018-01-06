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



class LDCOPpart3(LJAL):
    
    def __init__(self, num_edge=7, binary=False, n_dcop = 100):
        self.num_edge = num_edge
        self.binary = binary
        self.n_dcop = n_dcop
        
        toplevel_IL_graph = Graph(num_edge)
        super(LDCOPpart3, self).__init__(graph=toplevel_IL_graph, n_actions=num_edge, optimistic=0.0)

    def _get_graph(self, actions):
        graph = Graph(self.num_edge)
        if self.binary:
            for i, a in enumerate(actions):
                a1 = a // self.num_edge
                a2 =  a % self.num_edge
                graph.add_arc(i,a1)
                graph.add_arc(i,a2)
        else:
            for i, a in enumerate(actions):
                graph.add_arc(i,a)

        return graph

    def reward(self, actions):
        print(self.step)
        graph = self._get_graph(actions)
        def myDCOP(i):
            return DCOPpart2(graph=graph).n_steps(200)[-1]

        res = np.mean(list(parmap(myDCOP, range(self.n_dcop))))

        return res

    def temperature(self):
        return 1000* 0.994 ** self.step

    def alpha(self):
        return 0.5

parser = argparse.ArgumentParser(description='Part 3.')
parser.add_argument('-ndcop', dest='n_dcop_samples', type=int, default=100,
                    help='number of samples for the internal DCOP (default: 10)')
parser.add_argument('--save', dest='save_name', type=str, default="part3.pickle",
                    help='the filename of the plot (default: "part3.pickle")')

args = parser.parse_args()
    
steps = 1500

print("Running optLJAL-1")
start = timer()
ldcop = LDCOPpart3(n_dcop = args.n_dcop_samples)
Rs = ldcop.n_steps(steps)
end = timer()
optLJAL1_time = end - start

todo = todo = [{ "msg": "Running optLJAL-1", "name": "optLJAL-1", "fun":None, 
                 "partners": 0, "n_samples": 1, "Rs": Rs, "time": optLJAL1_time, "graph": ldcop.actions }]

with open(args.save_name, 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    pickle.dump(todo, f, pickle.HIGHEST_PROTOCOL)
