from random import randrange, random, seed
from unittest import TestCase

from Logic.DiGraph import DiGraph
from Logic.GraphAlgo import GraphAlgo


class TestGraphAlgo(TestCase):
    def test_get_graph(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A0.json')
        algo2 = GraphAlgo()
        algo2.graph = algo.get_graph()
        self.assertTrue(algo2.graph.v_size() == 11)
        self.assertTrue(algo2.graph.e_size() == 22)

    def test_load_from_json(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A0.json')
        self.assertTrue(algo.graph.v_size() == 11)
        self.assertTrue(algo.graph.e_size() == 22)

    def test_save_to_json(self):
        graph = DiGraph()
        graph.add_node(0, (50.0, 20.0))
        graph.add_node(1, (50.0, 0.0))
        graph.add_node(2, (0.0, 33.0))
        graph.add_node(3, (25.0, 0.0))
        graph.add_edge(0, 1, 2)
        graph.add_edge(1, 2, 5)
        graph.add_edge(2, 3, 4)
        graph.add_edge(3, 0, 9)
        algo = GraphAlgo()
        algo.graph = graph
        algo.save_to_json('../data/test.json')
        algo.load_from_json('../data/test.json')
        self.assertTrue(algo.graph.v_size() == 4)
        self.assertTrue(algo.graph.e_size() == 4)


    def test_is_connected(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A0.json')
        self.assertTrue(algo.is_connected())
        algo.load_from_json('../data/A1.json')
        self.assertTrue(algo.is_connected())
        algo.load_from_json('../data/A2.json')
        self.assertTrue(algo.is_connected())
        algo.load_from_json('../data/A3.json')
        self.assertTrue(algo.is_connected())
        algo.load_from_json('../data/A4.json')
        self.assertTrue(algo.is_connected())
        algo.load_from_json('../data/A5.json')
        self.assertTrue(algo.is_connected())
        algo.load_from_json('../data/T0.json')
        self.assertFalse(algo.is_connected())
        algo.load_from_json('../data/1000Nodes.json')
        self.assertTrue(algo.is_connected())
        algo.load_from_json('../data/10000Nodes.json')
        self.assertTrue(algo.is_connected())
    #
    #
    #
    def test_shortest_path(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A0.json')
        self.assertEqual(algo.shortest_path(3, 8)[1], [3, 4, 5, 6, 7, 8])
        self.assertEqual(algo.shortest_path(3, 8)[0], 7.286831393469998)
    #
    def test_tsp(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A0.json')

        # path, dist = algo.TSP([1, 2, 3, 4, 5, 6, 7])
        # algo.load_from_json('../data/A1.json')
        # path, dist = algo.TSP([1, 2, 3, 4, 5, 6, 7])
        # algo.load_from_json('../data/A2.json')
        # path, dist = algo.TSP([1, 2, 3, 4, 5, 6, 7])
        # algo.load_from_json('../data/A3.json')
        # path, dist = algo.TSP([1, 2, 3, 4, 5, 6, 7])
        # algo.load_from_json('../data/A4.json')
        # path, dist = algo.TSP([1, 2, 3, 4, 5, 6, 7])
        # algo.load_from_json('../data/A5.json')
        # path, dist = algo.TSP([1, 2, 3, 4, 5, 6, 7])
        self.assertEqual(algo.TSP([3, 8])[1], 7.286831393469998)
        self.assertEqual(algo.TSP([3, 8, 4, 7])[1], 17.58122129767496)

    # def graph_creator(self, num_of_nodes: int, num_of_ed: int):
    #     seed(1)
    #     graph = DiGraph()
    #     i = 0
    #     while i < num_of_nodes:
    #         graph.add_node(i)
    #         i = i + 1
    #     while graph.e_size() < num_of_ed:
    #         rnd = randrange(0, num_of_nodes)
    #         rnd2 = randrange(0, num_of_nodes)
    #         rnd3 = random()
    #         graph.add_edge(rnd, rnd2, rnd3 * 100)
    #     return graph
    #
    def test_center_point(self):
        algo = GraphAlgo()
        algo.load_from_json('../data/A0.json')
        self.assertTrue(algo.centerPoint()[0], 7)
        algo.load_from_json('../data/A1.json')
        self.assertTrue(algo.centerPoint()[0], 8)
        algo.load_from_json('../data/A2.json')
        self.assertEqual(algo.centerPoint()[0], 0)
        algo.load_from_json('../data/A3.json')
        self.assertTrue(algo.centerPoint()[0], 2)
        algo.load_from_json('../data/A4.json')
        self.assertTrue(algo.centerPoint()[0], 6)
        algo.load_from_json('../data/A5.json')
        self.assertTrue(algo.centerPoint()[0], 40)

