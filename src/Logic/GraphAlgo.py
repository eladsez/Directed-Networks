from API.GraphAlgoInterface import GraphAlgoInterface
import json
import sys
from typing import List
from DiGraph import DiGraph
from queue import Queue
from PriorityQueue import PriorityQueue


class GraphAlgo(GraphAlgoInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self, graph: DiGraph = None):
        if graph == None:
            self.graph = DiGraph()
        else:
            self.graph = graph

    def get_graph(self) -> DiGraph:
        """
        :return: the directed graph on which the algorithm works on.
        """
        return self.graph

    def load_from_json(self, file_name: str) -> bool:
        """
        Loads a graph from a json file.
        @param file_name: The path to the json file
        @returns True if the loading was successful, False o.w.
        """
        if self.graph != None:
            self.graph = DiGraph()
        try:
            with open(file_name, "r") as f:
                graph_dict = json.load(f)
                for node in graph_dict["Nodes"]:
                    try:
                        pos = tuple(node["pos"].split(","))
                        self.graph.add_node(node["id"], pos)
                    except:
                        self.graph.add_node(node["id"])

                for edge in graph_dict["Edges"]:
                    self.graph.add_edge(edge["src"], edge["dest"], edge["w"])
                return True
        except FileNotFoundError:
            print(FileNotFoundError)
            return False

    def save_to_json(self, file_name: str) -> bool:
        """
        Saves the graph in JSON format to a file
        @param file_name: The path to the out file
        @return: True if the save was successful, False o.w.
        """
        try:
            with open(file_name, 'w') as f:
                f.write(self.graph.__str__())
            return True
        except Exception:
            print(Exception)
            return False

    def transpose(self) -> DiGraph:
        trans_graph = DiGraph()
        for count, node_id in enumerate(self.graph.nodes):
            try:
                pos = (self.graph.nodes.get(node_id).pos[0], self.graph.nodes.get(node_id).pos[1])
                trans_graph.add_node(node_id, pos)
            except:
                trans_graph.add_node(node_id)

        for count, (src, dest) in enumerate(self.graph.edges):
            trans_graph.add_edge(dest, src, self.graph.edges[(src, dest)])

        return trans_graph

    # 0 - unvisited ,  1 - in progress,  2 - visited
    def bfs(self, src: int, graph: DiGraph) -> int:
        node_counter = 1  # set to 1 not to 0 because we already count the src
        queue = Queue(self.graph.v_size())
        for i, node in enumerate(graph.nodes.values()):
            node.tag = 0
        graph.nodes.get(src).tag = 1

        queue.put(graph.nodes.get(src))
        curr_node = adj_node = None
        while not queue.empty():
            curr_node = queue.get()
            for i, adj in enumerate(curr_node.edge_out):
                adj_node = graph.nodes.get(adj)
                if adj_node.tag == 0:
                    node_counter += 1
                    adj_node.tag = 1
                    queue.put(adj_node)
            curr_node.tag = 2

        return node_counter

    def is_connected(self) -> bool:
        trans = self.transpose()
        src_id = list(self.graph.nodes.values()).pop().id
        return self.bfs(src_id, self.graph) == self.graph.v_size() == self.bfs(src_id, trans)

    # node.tag used for the distance, node.dad used for the prev node
    def dijkstra(self, src: int):
        pq = PriorityQueue()
        # init the distance of all the nodes
        for i, node in enumerate(self.graph.nodes.values()):
            if node.id == src:
                node.tag = 0
                pq.enqueue(node)
            else:
                node.tag = sys.float_info.max
                pq.enqueue(node)

        curr_node = adj_node = None
        while not pq.is_empty():
            curr_node = pq.dequeue()
            for i, (adj_id, w) in enumerate(curr_node.edge_out.items()):
                adj_node = self.graph.nodes.get(adj_id)

                if adj_node.tag > curr_node.tag + w:
                    adj_node.tag = curr_node.tag + w
                    adj_node.dad = curr_node.id
                    temp = adj_node
                    pq.pq.remove(adj_node)
                    pq.enqueue(temp)

    def shortest_path(self, id1: int, id2: int) -> (float, list):
        """
        Returns the shortest path from node id1 to node id2 using Dijkstra's Algorithm
        @param id1: The start node id
        @param id2: The end node id
        @return: The distance of the path, a list of the nodes ids that the path goes through
        Example:
#      >>> from GraphAlgo import GraphAlgo
#       >>> g_algo = GraphAlgo()
#        >>> g_algo.addNode(0)
#        >>> g_algo.addNode(1)
#        >>> g_algo.addNode(2)
#        >>> g_algo.addEdge(0,1,1)
#        >>> g_algo.addEdge(1,2,4)
#        >>> g_algo.shortestPath(0,1)
#        (1, [0, 1])
#        >>> g_algo.shortestPath(0,2)
#        (5, [0, 1, 2])
        Notes:
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        More info:
        https://en.wikipedia.org/wiki/Dijkstra's_algorithm
        """
        nodes_id = list(self.graph.nodes.keys())
        if (not id1 in nodes_id) or (not id2 in nodes_id):
            return float('inf'), []

        self.dijkstra(id1)

        if (self.graph.nodes.get(id2).tag == sys.float_info.max):
            return float('inf'), []

        path = []
        path.append(id2)
        curr_node = self.graph.nodes.get(id2).dad
        while (curr_node != id1):
            path.append(curr_node)
            curr_node = self.graph.nodes.get(curr_node).dad
        path.append(id1)
        path.reverse()

        return self.graph.nodes.get(id2).tag, path

    def add_help_nodes(self, node_list: List[Node]):
        assembled_route = []
        added_nodes = []
        j = None
        for i in range(0, len(node_list)):
            j = i + 1
            added_nodes.clear()
            added_nodes.extend(self.shortest_path(node_list[i].id, node_list[j].id)[1])
            if i > 0:
                added_nodes.pop(0)
                assembled_route.extend(added_nodes)
            else:
                assembled_route.extend(added_nodes)

        return assembled_route

    def rout_dist(self, node_list: List[Node]):
        dist = 0
        j = None
        for i in range(0, len(node_list)):
            curr_dist = self.shortest_path(node_list[i].id, node_list[j].id)[0]
            dist += curr_dist

        return dist

    def make_new_route(self, node_list: List[Node], node1: Node, node2: Node):
        assembled_route = List.copy(node_list)
        node1_to_node2 = []
        route_end = []

        # coping the end nodes
        for i in range(len(assembled_route) - 1, node2):
            route_end.append(assembled_route.pop(i))
        List.reverse(route_end)

        # coping and reversing the order of all the nodes from node1 to node2
        for i in range(node2, node1):
            node1_to_node2.append(assembled_route.pop(i))

        # rebuilt the list middle
        assembled_route.extend(node1_to_node2)

        # rebuild the list end
        assembled_route.extend(route_end)

        return assembled_route

    def TSP(self, node_lst: List[int]) -> (List[int], float):
        """
        Finds the shortest path that visits all the nodes in the list
        :param node_lst: A list of nodes id's
        :return: A list of the nodes id's in the path, and the overall distance
        """
        # run only on connected graphs, with 1 node minimum
        if self.is_connected() or self.graph.v_size() == 0:
            return None

        existing_route = List.copy(node_lst)
        existing_route = self.add_help_nodes(existing_route)
        new_route = []
        tmp2 = []
        tmp1 = List.copy(node_lst)
        best_dist = self.rout_dist(existing_route)

        for i in range(1, len(node_lst) - 1):
            for j in range(i + 1, len(node_lst)):
                tmp2 = List.copy(tmp1)
                tmp1 = self.make_new_route(tmp2, i, j)
                new_route = self.add_help_nodes(tmp1)
                new_dist = self.rout_dist(new_route)
                if new_dist < best_dist:
                    existing_route = new_route
                    best_dist = new_dist
                else:
                    tmp1 = tmp2

        return existing_route

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        if not self.is_connected(): return None, sys.float_info.max
        center_id = None
        min_dist = sys.float_info.max
        curr_dist = None
        for i, node_id in enumerate(self.graph.nodes.keys()):
            curr_dist = self.farest_dist(node_id, min_dist)
            if curr_dist < min_dist:
                min_dist = curr_dist
                center_id = node_id

        return center_id, min_dist

    def farest_dist(self, src: int, curr_min_dist: float) -> float:
        max_dist = sys.float_info.min
        curr_dist = None
        for i, node_id in enumerate(self.graph.nodes.keys()):
            if node_id == src: continue
            curr_dist = self.shortest_path(src, node_id)[0]

            if curr_dist > max_dist:
                max_dist = curr_dist

            if curr_dist > curr_min_dist:
                break

        return max_dist

    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """

        raise NotImplementedError


if __name__ == '__main__':
    # graph = GraphInterface()
    # graph.add_node(0, (50.0, 20.0))
    # graph.add_node(1, (50.0, 0.0))
    # graph.add_node(2, (0.0, 33.0))
    # graph.add_node(3, (25.0, 0.0))
    # graph.add_edge(0, 1, 2)
    # graph.add_edge(1, 2, 5)
    # graph.add_edge(2, 3, 4)
    # graph.add_edge(3, 0, 9)
    # print(graph.__str__())
    algo = GraphAlgo()
    # print(algo.shortest_path(0,3))
    # trans = algo.transpose()
    # print(trans.__str__())
    algo.load_from_json("../../Data/A0.json")
    # print(algo.shortest_path(5,30))
    print(algo.centerPoint())
    # print(algo.is_connected())
    # print(algo.save_to_json("bla.json"))
