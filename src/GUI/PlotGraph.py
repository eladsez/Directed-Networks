import random
import sys
import matplotlib.pyplot as plt
from Logic.DiGraph import DiGraph


class PlotView:
    def __init__(self, graph: DiGraph):
        self.node_x_pos = {}  # (node_id, x_pos)
        self.node_y_pos = {}  # (node_id, y_pos)
        self.graph = graph

    # init the pos of the nodes which doesnt has location pos
    def update_scale(self):
        min_x = min_y = sys.float_info.min
        max_x = max_y = sys.float_info.max
        node_list = enumerate(self.graph.nodes.values())

        for i, node in node_list:
            print(node)
            if node.pos == None: continue
            self.node_x_pos[node.id] = node.pos[0]
            self.node_y_pos[node.id] = node.pos[1]
            if node.pos[0] < min_x: min_x = node.pos[0]
            if node.pos[1] < min_y: min_y = node.pos[1]
            if node.pos[0] > max_x: max_x = node.pos[0]
            if node.pos[1] > max_y: max_y = node.pos[1]

        for i ,node in node_list:
            if node.pos == None:
                self.node_x_pos[node.id] = random.uniform(min_x, max_x)
                self.node_y_pos[node.id] = random.uniform(min_y, max_y)

        print(len(self.node_x_pos))

        for i, x in enumerate(self.node_x_pos.values()):
            print(x)

        plt.xlim(min_x, max_x), plt.ylim(min_y, max_y)

    def draw_graph(self):
        for node in list(self.graph.nodes.values()):
            x = float(self.node_x_pos[node.id])
            y = float(self.node_y_pos[node.id])
            plt.plot(x, y, markersize=10, marker="o", color="green")

        for ((src, dest), w) in (self.graph).edges.items():
            x1 = float(self.node_x_pos[src])
            y1 = float(self.node_y_pos[src])
            x2 = float(self.node_x_pos[dest])
            y2 = float(self.node_y_pos[dest])
            plt.annotate("", xy=(x1, y1), xytext=(x2, y2), arrowprops={"arrowstyle": "<-", "lw": 2})
        plt.show()