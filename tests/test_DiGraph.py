from unittest import TestCase
from Logic.DiGraph import DiGraph
from Logic.GraphAlgo import GraphAlgo

class TestDiGraph(TestCase):

    def test_v_size(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A0.json')
        self.assertTrue(algo.graph.v_size() == 11)

    def test_e_size(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A0.json')
        self.assertTrue(algo.graph.e_size() == 22)

    # def test_get_all_v(self):
    #     self.fail()
    #
    # def test_add_edge(self):
    #     self.fail()
    #
    # def test_add_node(self):
    #     self.fail()
    #
    # def test_remove_node(self):
    #     self.fail()
    #
    # def test_remove_edge(self):
    #     self.fail()
