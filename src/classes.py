
class Node:
    def __init__(self, id:int, pos:tuple):
        self.id = id
        self.edge_in = dict[int, float]({})
        self.edge_out = dict[int, float]({})
        self.tag = None
        self.pos = pos
