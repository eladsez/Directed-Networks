from functools import cmp_to_key

from API.GraphAlgoInterface import GraphAlgoInterface
import json
import sys
from typing import List
from Logic.DiGraph import DiGraph
from queue import Queue
from Logic.Node import Node
from Logic.PriorityQueue import PriorityQueue
from GUI.PlotGraph import PlotView
from Logic.UnionFind import UnionFind


class GraphAlgo(GraphAlgoInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self, graph: DiGraph = None):
        if graph is None:
            self.graph = DiGraph()
        else:
            self.graph = graph
        self.plot = None

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
        if self.graph is not None:
            self.graph = DiGraph()
        try:
            with open(file_name, "r") as f:
                graph_dict = json.load(f)
                for node in graph_dict["Nodes"]:
                    try:
                        pos = tuple(node["pos"].split(","))
                        self.graph.add_node(int(node["id"]), (float(pos[0]), float(pos[1])))
                    except:
                        self.graph.add_node(node["id"])

                for edge in graph_dict["Edges"]:
                    self.graph.add_edge(int(edge["src"]), int(edge["dest"]), float(edge["w"]))
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
            raise Exception
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
        """`isConnected` - return whether the graph is strongly connected or not.
            We've implemented the algorithm in the following way:
              1. Run BFS algorithms from a specific node to all of the other nodes
              2. Run BFS again, this time on the graph transposed.
              3. Check if the BFS's results are equals to each othe and to the nuber of nodes in the graph.
              4. If so - the graph is strongly connected.   """
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
        If there is no path between id1 and id2, or one of them dose not exist the function returns (float('inf'),[])
        """
        """`shortestPath` - return the shortest path between two nodes.  
            We've implemented the algorithm in the following way:    
              1. Run DIJKSTRA algorithm on the source node - in order to get in each node the shortest path from the source, 
                and the distance. 
              2. Because each node tag "carry" the node that came before it in the path, 
                all there is to do is to loop from the destination node and ask who came before until we get to the source node.
              3. The results are then inserted into a list and returned """
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
        tmp = []
        added_nodes = []
        i = 0
        j = 1
        while i < len(node_list) and j < len(node_list):
            tmp.clear()
            added_nodes.clear()
            tmp.extend(self.shortest_path(node_list[i].id, node_list[j].id)[1])
            for k in tmp:
                added_nodes.append(self.graph.nodes[k])

            if i > 0:
                added_nodes.pop(0)
                assembled_route.extend(added_nodes)
            else:
                assembled_route.extend(added_nodes)
            i += 1
            j += 1

        return assembled_route

    def rout_dist(self, node_list: List[Node]):
        dist = 0
        j = 1
        i = 0
        while j < len(node_list):
            curr_dist = self.shortest_path(node_list[i].id, node_list[j].id)[0]
            dist += curr_dist
            i += 1
            j += 1

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
        """ `tsp` - return the shortest path between a list of nodes.   
            **Approach:** we are using swapping algorithm, in order to get an acceptable path at reasonable time.
            We've implemented the algorithm in the following way:    
              1. Start with a random route that start in the source node.
              2. Perform a swap between nodes (except the source).
              3. Keep new route if it is shorter.
              4. Repeat (2-3) for all possible swaps.
            since in this assignment we are not required to return to the source node it's simplify the solution a bit.  
            This algorithm is both faster, O(M*N^2) and produces better solutions then greedy algorithm.  
            The intuition behind the algorithm is that, 
            swapping untangles routes that cross over itself (gets rid of circle's when possible).  
            This swap algorithm performed much better than greedy; 
            the path it drew looks similar to something a human might draw. """
        # run only on connected graphs, with 1 node minimum
        if not self.is_connected() or self.graph.v_size() == 0:
            return None

        actual_nodes = []
        for i in node_lst:
            actual_nodes.append(self.graph.nodes[i])

        existing_route = List.copy(actual_nodes)
        existing_route = self.add_help_nodes(existing_route)
        new_route = []
        tmp2 = []
        tmp1 = List.copy(actual_nodes)
        best_dist = self.rout_dist(existing_route)

        for i in range(1, len(actual_nodes) - 1):
            for j in range(i + 1, len(actual_nodes)):
                tmp2 = List.copy(tmp1)
                tmp1 = self.make_new_route(tmp2, i, j)
                new_route = self.add_help_nodes(tmp1)
                new_dist = self.rout_dist(new_route)
                if new_dist < best_dist:
                    existing_route = new_route
                    best_dist = new_dist
                else:
                    tmp1 = tmp2

        ans = []
        for i in existing_route:
            ans.append(i.id)

        return existing_route, best_dist

    def centerPoint(self) -> (int, float):
        """
        Finds the node that has the shortest distance to it's farthest node.
        :return: The nodes id, min-maximum distance
        """
        """ `center` - return the node that is the closest to every other node.   
            **Approach:** we are searching for the node with the shortest path, 
            but from the longest result this node got from `shortestPathDist`.
            We've implemented the algorithm in the following way:    
              1. Loop through all of the nodes in the graph.
              2. For each node check with `shortestPathDist` what is the **longest** path
              3. Return the node with the shortest one. """
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

    def kruskal_MST(self) -> List[tuple]:
        """
        This method is an implementation of the kruskal minimum spanning tree algorithm
        by using the union find data structure
        :return: a list representing all the edges in the MST by tuple of (src_node_id, dest_node_id)
        """
        mts = []
        edges = dict(sorted(self.graph.get_all_e().items(), key=lambda item: item[1]))
        nodes = self.graph.get_all_v()
        sets = UnionFind()
        for node_id, node in nodes.items():
            sets.make_set(node_id)

        for (src, dest), w in edges.items():
            if sets.find(src) != sets.find(dest):
                mts.append((src, dest))
                sets.union(src, dest)

        return mts

    # To find orientation of ordered triplet (p, q, r).
    # The function returns following values
    # 0 --> p, q and r are collinear
    # 1 --> Clockwise
    # -1 --> Counterclockwise
    def orientation(self, p: Node, q: Node, r: Node):
        val = ((q.pos[1] - p.pos[1]) * (r.pos[0] - q.pos[0]) -
               (q.pos[0] - p.pos[0]) * (r.pos[1] - q.pos[1]))
        if val == 0:
            return 0  # collinear
        elif val > 0:
            return 1  # clock wise
        else:
            return -1  # counterclock wise

    # A utility function to return square of distance
    # between p1 and p2
    def distSq(self, p1, p2):
        return ((p1.pos[0] - p2.pos[0]) * (p1.pos[0] - p2.pos[0]) +
                (p1.pos[1] - p2.pos[1]) * (p1.pos[1] - p2.pos[1]))

    # A function used by cmp_to_key function to sort an array of
    # points with respect to the first point
    def compare(self, p1, p2):
        global start_node
        # Find orientation
        o = self.orientation(start_node, p1, p2)
        if o == 0:
            if self.distSq(start_node, p2) >= self.distSq(start_node, p1):
                return -1
            else:
                return 1
        else:
            if o == -1:
                return -1
            else:
                return 1

    def convex_hull(self):
        nodes = list(self.graph.get_all_v().values())
        if len(nodes) < 3:
            return
        global start_node
        start_node = max(nodes, key=lambda node: node.pos[1])
        nodes.remove(start_node)
        nodes.sort(key=cmp_to_key(self.compare))
        stack = [start_node, nodes[0], nodes[1]]
        for i in range(2, len(nodes)):
            while len(stack) > 1 and self.orientation(stack[-2], stack[-1], nodes[i]) != -1:
                stack.pop()
            stack.append(nodes[i])

        for i in range(1, len(stack)):
            self.graph.add_edge(stack[i - 1].id, stack[i].id, 0)
        self.graph.add_edge(stack[0].id, stack[-1].id, 0)


    def plot_graph(self) -> None:
        """
        Plots the graph.
        If the nodes have a position, the nodes will be placed there.
        Otherwise, they will be placed in a random but elegant manner.
        @return: None
        """

        self.plot = PlotView(self.graph)
        self.plot.update_scale()
        self.plot.draw_graph()


if __name__ == '__main__':
    algo = GraphAlgo()
    algo.load_from_json("../../Data/A0.json")
    print(algo.convex_hull())
