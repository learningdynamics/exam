from ljal import *

class DCOPpart2(LJAL):
    def __init__(self,graph):
        # set n_actions=2, because of the binary constraints
        super(DCOPpart2,self).__init__(graph=graph,n_actions=4)

    def set_weight_mat(self):
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




    def set_reward(self,weight_mat):
        # the reward matrix is a 4*4*$C_7^2$ matrix
        reward_mat = np.zeros([self.n_agents**2])
        for i in range(self.n_agents):
            for j in range(0,i):
                temp_mat = np.random.normal(0,self.n_agents*10*weight_mat[i,j],size=[self.n_actions,self.n_actions])
                reward_mat[i][j] = temp_mat
                reward_mat[j][i] = temp_mat










class TestDCOPMethod(unittest.TestCase):

    def testSetReward(self):
        pass

