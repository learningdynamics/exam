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
