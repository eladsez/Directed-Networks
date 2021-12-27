from Logic.Node import Node
from API.GraphInterface import GraphInterface


class DiGraph(GraphInterface):
    """This abstract class represents an interface of a graph."""

    def __init__(self):
        self.nodes = {}  # (nodeID, node)
        self.edges = {}  # ((src,dest), w)
        self.MC = 0

    def v_size(self) -> int:
        """
        Returns the number of vertices in this graph
        @return: The number of vertices in this graph
        """
        return len(self.nodes)

    def e_size(self) -> int:
        """
        Returns the number of edges in this graph
        @return: The number of edges in this graph
        """
        return len(self.edges)

    def get_all_v(self) -> dict:
        """return a dictionary of all the nodes in the Graph, each node is represented using a pair
         (node_id, node_data)
        """
        return self.nodes

    def all_in_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected to (into) node_id ,
        each node is represented using a pair (other_node_id, weight)
         """
        return self.nodes.get(id1).edge_in

    def all_out_edges_of_node(self, id1: int) -> dict:
        """return a dictionary of all the nodes connected from node_id , each node is represented using a pair
        (other_node_id, weight)
        """
        return self.nodes.get(id1).edge_out

    def get_mc(self) -> int:
        """
        Returns the current version of this graph,
        on every change in the graph state - the MC should be increased
        @return: The current version of this graph.
        """
        return self.MC

    def add_edge(self, id1: int, id2: int, weight: float) -> bool:
        """
        Adds an edge to the graph.
        @param id1: The start node of the edge
        @param id2: The end node of the edge
        @param weight: The weight of the edge
        @return: True if the edge was added successfully, False o.w.
        Note: If the edge already exists or one of the nodes dose not exists the functions will do nothing
        """
        if id1 in self.nodes.keys() and id2 in self.nodes.keys():
            self.nodes[id1].edge_out[id2] = weight
            self.nodes[id2].edge_in[id1] = weight
            self.edges[(id1, id2)] = weight
            self.MC += 1
            return True
        else:
            return False

    def add_node(self, node_id: int, pos: tuple = None) -> bool:
        """
        Adds a node to the graph.
        @param node_id: The node ID
        @param pos: The position of the node
        @return: True if the node was added successfully, False o.w.
        Note: if the node id already exists the node will not be added
        """
        if node_id in self.nodes.keys():
            return False
        else:
            self.nodes[node_id] = Node(node_id, pos)
            self.MC += 1
            return True

    def remove_node(self, node_id: int) -> bool:
        """
        Removes a node from the graph.
        @param node_id: The node ID
        @return: True if the node was removed successfully, False o.w.
        Note: if the node id does not exists the function will do nothing
        """
        if node_id in self.nodes.keys():
            self.nodes.pop(node_id)

            for i, node in enumerate(self.nodes.values()):
                if node_id in node.edge_in.keys():
                    node.edge_in.pop(node_id)
                if node_id in node.edge_out.keys():
                    node.edge_out.pop(node_id)

            for (src, dest) in list(self.edges):
                if src == node_id or dest == node_id:
                    self.edges.pop((src, dest))

            self.MC += 1
            return True

        else:
            return False

    def remove_edge(self, node_id1: int, node_id2: int) -> bool:
        """
        Removes an edge from the graph.
        @param node_id1: The start node of the edge
        @param node_id2: The end node of the edge
        @return: True if the edge was removed successfully, False o.w.
        Note: If such an edge does not exists the function will do nothing
        """
        if node_id1 in self.nodes and node_id2 in self.nodes:
            if node_id1 in self.nodes[node_id2].edge_in and node_id2 in self.nodes[node_id1].edge_out:
                self.nodes[node_id1].edge_out.pop(node_id2)
                self.nodes[node_id2].edge_in.pop(node_id1)
                self.MC += 1
                self.edges.pop((node_id1, node_id2))
                return True
        return False

    def __str__(self):
        ans = "{\n\"Edges\": [\n"

        edgeiter = enumerate(self.edges)
        for key, edge in edgeiter:
            ans += "{\n" + "\"src\": " + str(edge[0]) + ",\n" + "\"w\": " + str(
                self.edges[edge[0], edge[1]]) + ",\n" + "\"dest\": " + str(edge[1]) + "\n" + "}"
            if key == len(self.edges) - 1:
                ans += "\n"
                break
            else:
                ans += ",\n"

        ans += "],\n\"Nodes\": ["
        nodeiter = enumerate(self.nodes)
        for key, nodeID in nodeiter:
            if self.nodes[nodeID].pos is not None:
                ans += "{\n\"pos\": " + "\"" + str(self.nodes[nodeID].pos[0]) + "," + str(
                        self.nodes[nodeID].pos[1]) + ",0.0\"" + ",\n\"id\": " + str(nodeID) + "\n}"
            if key == len(self.nodes) - 1:
                ans += "\n"
                break
            else:
                ans += ",\n"

        ans += "]\n}"
        return ans


if __name__ == '__main__':
    graph = DiGraph()
    graph.add_node(0, (50.0, 20.0))
    graph.add_node(1, (50.0, 0.0))
    graph.add_node(2, (0.0, 33.0))
    graph.add_node(3, (25.0, 0.0))
    graph.add_node(4, (0.0, 0.0))
    graph.add_node(5, (0, 0))
    graph.add_node(6, (0, 0))
    graph.add_edge(0, 3, 2)
    graph.add_edge(0, 2, 5)
    graph.add_edge(0, 5, 4)
    graph.add_edge(1, 3, 9)
    print(graph.__str__())
    graph.remove_node(0)
    print(graph.__str__())

