from ljal import *
import sys
from timeit import default_timer as timer
from multiprocessing import Pool
import matplotlib.pyplot as plt
import tasks
import argparse



class DCOPpart2(LJAL):
    def __init__(self, graph):
        super(DCOPpart2, self).__init__(graph=graph, n_actions=4, optimistic=0.0)

        self.rewards = self._set_reward(self._set_weight_mat())


    def _set_weight_mat(self):
        # here we use the structure in the paper Fig 5
        weight_mat = np.full([self.n_agents,self.n_agents], 0.1)
        # constriants for (1,2),(1,3),(2,3), (5,6) are important
        # the matrix are symmetric, we use the half triangular
        for (i,j) in [(0,1),(0,2),(1,2),(4,5)]:
            weight_mat[i,j] = 0.9
            weight_mat[j,i] = 0.9
        for i in  range(self.n_agents):
            weight_mat[i,i] = 0

        return weight_mat



    def _set_reward(self,weight_mat):
        # the reward matrix is a 4*4*$C_7^2$ matrix
        reward_mat = [[0 for i in range(7)] for j in range(7)]
        for i in range(self.n_agents):
            for j in range(0,i):
                temp_mat = np.random.normal(0,self.n_agents*10*weight_mat[i,j],size=[self.n_actions,self.n_actions])
                reward_mat[i][j] = temp_mat
                reward_mat[j][i] = temp_mat
        return reward_mat

    def reward(self, actions):
        # the reward is the sum of the reward
        s = 0
        for i in range(self.n_agents-1):
            for j in range(i+1,self.n_agents):
                s += self.rewards[i][j][actions[i]][actions[j]]
        return s

    def temperature(self):
        return 1000* 0.94 ** self.step

    def alpha(self):
        return 0.5


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
LJAL2_graph.add_arcs((0,1), (0,2), (1,0), (1,2), (2,0), (2,1), (4,5), (5,4))
LJAL3_graph = Graph(7)
LJAL3_graph.add_arcs((0,1),(0,2),(1,0),(1,2),(2,0),(2,1),(4,5),(5,4),(0,4),(4,0))
full_graph = FullGraph(7)
todo = [{ "msg": "Running IL", "name": "IL", "partners": 0, "n_samples": args.n_samples,
          "fun":lambda:  DCOPpart2(graph=Graph(7)).n_steps(steps)},
        { "msg": "Running LJAL-1", "name": "LJAL-1", "partners": 2, "n_samples": args.n_samples,
          "fun": lambda: DCOPpart2(graph=RandomGraph(7, 2)).n_steps(steps)},
        { "msg":"Running LJAL-2", "name": "LJAL-2", "partners": 1.14, "n_samples": args.n_samples,
          "fun": lambda: DCOPpart2(graph=LJAL2_graph).n_steps(steps)},
        { "msg":"Running LJAL-3", "name": "LJAL-3", "partners": 1.43, "n_samples": args.n_samples,
          "fun": lambda: DCOPpart2(graph=LJAL3_graph).n_steps(steps)},
        { "msg":"Running JAL", "name":"JAL", "partners": 6, "n_samples": args.n_jal_samples,
          "fun": lambda: DCOPpart2(graph=full_graph).n_steps(steps)}]


tasks.run(todo, args.save_name)



