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

    def test_get_all_v(self):
        graph = DiGraph()
        graph.add_node(0, (50.0, 20.0))
        graph.add_node(1, (50.0, 0.0))
        graph.add_node(2, (0.0, 33.0))
        graph.add_node(3, (25.0, 0.0))
        v_dict = graph.get_all_v()
        self.assertTrue(len(v_dict) == 4)
        self.assertEqual(v_dict.get(0).id, 0)
        self.assertEqual(v_dict.get(1).id, 1)
        self.assertEqual(v_dict.get(2).id, 2)
        self.assertEqual(v_dict.get(3).id, 3)


    def test_add_edge(self):
        graph = DiGraph()
        graph.add_node(0, (50.0, 20.0))
        graph.add_node(1, (50.0, 0.0))
        graph.add_node(2, (0.0, 33.0))
        graph.add_node(3, (25.0, 0.0))
        graph.add_edge(0, 1, 2)
        graph.add_edge(1, 2, 5)
        graph.add_edge(2, 3, 4)
        graph.add_edge(3, 0, 9)
        self.assertTrue(graph.e_size() == 4)
        graph.add_edge(2, 0, 4)
        graph.add_edge(3, 1, 9)
        self.assertTrue(graph.e_size() == 6)

    def test_add_node(self):
        graph = DiGraph()
        graph.add_node(0, (50.0, 20.0))
        graph.add_node(1, (50.0, 0.0))
        graph.add_node(2, (0.0, 33.0))
        graph.add_node(3, (25.0, 0.0))
        self.assertTrue(graph.v_size() == 4)
        graph.add_node(4, (25.0, 0.0))
        self.assertTrue(graph.v_size() == 5)

    def test_remove_node(self):
        graph = DiGraph()
        graph.add_node(0, (50.0, 20.0))
        graph.add_node(1, (50.0, 0.0))
        graph.add_node(2, (0.0, 33.0))
        graph.add_node(3, (25.0, 0.0))
        graph.add_edge(0, 1, 2)
        graph.add_edge(1, 2, 5)
        graph.add_edge(2, 3, 4)
        graph.add_edge(3, 0, 9)
        self.assertTrue(graph.v_size() == 4)
        graph.add_node(4, (25.0, 0.0))
        self.assertTrue(graph.v_size() == 5)
        graph.remove_node(4)
        self.assertTrue(graph.v_size() == 4)
        self.assertTrue(graph.e_size() == 4)
        graph.remove_node(2)
        self.assertTrue(graph.v_size() == 3)
        self.assertTrue(graph.e_size() == 2)

    def test_remove_edge(self):
        graph = DiGraph()
        graph.add_node(0, (50.0, 20.0))
        graph.add_node(1, (50.0, 0.0))
        graph.add_node(2, (0.0, 33.0))
        graph.add_node(3, (25.0, 0.0))
        graph.add_edge(0, 1, 2)
        graph.add_edge(1, 2, 5)
        graph.add_edge(2, 3, 4)
        graph.add_edge(3, 0, 9)
        self.assertTrue(graph.e_size() == 4)
        graph.add_edge(2, 0, 4)
        graph.add_edge(3, 1, 9)
        self.assertTrue(graph.e_size() == 6)
        graph.remove_edge(2, 0)
        graph.remove_edge(3, 1)
        self.assertTrue(graph.e_size() == 4)
