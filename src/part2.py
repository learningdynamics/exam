from ljal import *
import sys
from timeit import default_timer as timer
from multiprocessing import Pool
import matplotlib.pyplot as plt
import tasks
import argparse
from dcop import DCOPpart2


parser = argparse.ArgumentParser(description='Part 2.')
parser.add_argument('-n', dest='n_samples', type=int, default=100,
                    help='number of samples (default: 100)')
parser.add_argument('-njal', dest='n_jal_samples', type=int, default=10,
                    help='number of samples for JAL (default: 10)')
parser.add_argument('--save', dest='save_name', type=str, default="part2.pickle",
                    help='the filename of the plot (default: "part2.pickle")')

args = parser.parse_args()
    
steps = 200

LJAL2_graph = Graph(7)
LJAL2_graph.add_arcs((0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(4,5),(5,4))
LJAL3_graph = Graph(7)
LJAL3_graph.add_arcs((0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(4,5),(5,4),(0,4),(4,0))
LJAL4_graph = Graph(7)
LJAL4_graph.add_arcs((0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(4,5),(5,4),(3,6),(6,3))
full_graph = FullGraph(7)
todo = [{ "msg": "Running IL", "name": "IL", "partners": 0, "n_samples": args.n_samples,
          "fun":lambda:  DCOPpart2(graph=Graph(7)).n_steps(steps)},
        { "msg": "Running LJAL-1", "name": "LJAL-1", "partners": 2, "n_samples": args.n_samples,
          "fun": lambda: DCOPpart2(graph=RandomGraph(7, 2)).n_steps(steps)},
        { "msg":"Running LJAL-2", "name": "LJAL-2", "partners": 1.14, "n_samples": args.n_samples,
          "fun": lambda: DCOPpart2(graph=LJAL2_graph).n_steps(steps)},
        { "msg":"Running LJAL-3", "name": "LJAL-3", "partners": 1.43, "n_samples": args.n_samples,
          "fun": lambda: DCOPpart2(graph=LJAL3_graph).n_steps(steps)},
        { "msg":"Running LJAL-4", "name": "LJAL-4", "partners": 1.43, "n_samples": args.n_samples,
          "fun": lambda: DCOPpart2(graph=LJAL4_graph).n_steps(steps)},
        { "msg":"Running JAL", "name":"JAL", "partners": 6, "n_samples": args.n_jal_samples,
          "fun": lambda: DCOPpart2(graph=full_graph).n_steps(steps)}]


tasks.run(todo, args.save_name)



