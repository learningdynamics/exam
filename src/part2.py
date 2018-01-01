from ljal import *

class DCOPpart2(LJAL):
    def __init__(self,graph):
        super(DCOPpart2,self).__init__(graph=graph,n_actions=4)
        self.rewards = self._set_reward(self._set_weight_mat())

    def _set_weight_mat(self):
        # here we use the structure in the paper Fig 5
        weight_mat = np.zeros([self.n_agents,self.n_agents])+0.1
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

    def one_step(self):
        self.actions = np.array([BoltzmannAction(EVs(self.Qs[agent], self.Ns[agent]),
                                                temp=self.temperature())
                                for agent in range(0, self.n_agents)])
        for agent1 in range(len(self.n_agents)):
            for agent2 in range(agent1+1,len(self.n_agents)):
                    # every agent play with each other
                agent1_act = self.actions[agent1]
                agent2_act = self.actions[agent2]

                self.R = self.rewards[agent1][agent2][agent1_act][agent2_act]
                # update the Q and Ns for agent1
                x = agent1_act
                y = self._y(agent1,self.actions)

                self.Qs[agent1][x, y] += self.alpha * (self.R - self.Qs[agent1][x, y])
                self.Ns[agent1][x, y] += 1

                # update the Q and Ns for agent2
                x = agent1_act
                y = self._y(agent2, self.actions)

                self.Qs[agent2][x, y] += self.alpha * (self.R - self.Qs[agent2][x, y])
                self.Ns[agent2][x, y] += 1






a = Graph(7)
a.add_arc(0,1)
a.add_arc(0,2)
a.add_arc(0,3)
a.add_arc(4,5)
a.add_arc(4,6)







class TestDCOPMethod(unittest.TestCase):

    def testSetReward(self):
       pass



