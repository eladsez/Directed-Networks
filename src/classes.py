
class Node:
    def __init__(self, id:int, pos:tuple):
        self.id = id
        self.edge_in = {}
        self.edges_out = {}
        self.tag = None
        self.pos = pos


# class Edge:
#
#     def __init__(self, src:int, dest:int, weight:float):
#         self.src = src
#         self.dest = dest
#         self.weight = weight
#         self.tag = None
