import random
import sys
import matplotlib.pyplot as plt

from Logic.GraphAlgo import GraphAlgo


class PlotView:
    def __init__(self, algo: GraphAlgo):
        self.node_x_pos = {}  # (node_id, x_pos)
        self.node_y_pos = {}  # (node_id, y_pos)
        self.algo = algo

    # init the pos of the nodes which doesnt has location pos
    def update_scale(self):
        min_x = min_y = sys.float_info.min
        max_x = max_y = sys.float_info.max
        node_list = list(self.algo.graph.nodes.values())

        for node in node_list:
            if node.pos == None: continue
            self.node_x_pos[node.id] = node.pos[0]
            self.node_y_pos[node.id] = node.pos[1]
            if node.pos[0] < min_x: min_x = node.pos[0]
            if node.pos[1] < min_y: min_y = node.pos[1]
            if node.pos[0] > max_x: max_x = node.pos[0]
            if node.pos[1] > max_y: max_y = node.pos[1]

        for node in node_list:
            if node.pos == None:
                self.node_x_pos[node.id] = random.uniform(min_x, max_x)
                self.node_y_pos[node.id] = random.uniform(min_y, max_y)

        plt.xlim(min_x, max_x), plt.ylim(min_y, max_y)

    def draw_graph(self):
        pass


if __name__ == '__main__':
    algo = GraphAlgo()
    algo.load_from_json("../Data/A0.json")
    for node in list(algo.graph.nodes.values()):
        pass

    plt.show()
