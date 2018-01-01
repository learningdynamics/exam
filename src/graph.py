#! /usr/bin/python3

import unittest

class Graph(object):

    def __init__(self, n_nodes):
        self.nodes = [{} for i in range(0,n_nodes)]

    def add_arc(self, src, dst, weigth = 1):
        if (src != dst):
            self.nodes[src][dst] = weigth

    def successors(self, node):
        return sorted(self.nodes[node].keys())


####################
## TESTING
class TestGraphMethods(unittest.TestCase):


    def test_Graph(self):
        g = Graph(10)
        self.assertTrue(isinstance(g.nodes[0],dict))

    def test_add_arc(self):
        print("arc")
        g = Graph(10)
        g.add_arc(1,1)
        g.add_arc(1,2)
        g.add_arc(1,5)
        self.assertTrue(2 in g.nodes[1])
        self.assertTrue(5 in g.nodes[1])
        self.assertFalse(1 in g.nodes[1])

    def test_add_arc1(self):
        g = Graph(10)
        g.add_arc(1,2)
        g.add_arc(1,5)
        self.assertEqual([2,5], g.successors(1))

if __name__ == "__main__":
    unittest.main()

#unittest.main()

