
class Node:
    def __init__(self, id:int, pos:tuple):
        self.id = id
        self.edge_in = dict[int, float]({}) # (src, w)
        self.edge_out = dict[int, float]({}) # (dest, w)
        self.tag = None
        self.pos = pos
