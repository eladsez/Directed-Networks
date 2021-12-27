class Node:
    def __init__(self, id: int, pos: tuple):
        self.id = id
        self.edge_in = {}  # (src, w)
        self.edge_out = {}  # (dest, w)
        self.tag = None
        self.dad = None
        self.pos = pos

    # compare for priority queue in dijkstra
    def __lt__(self, other):
        return self.tag < other.tag

    def __repr__(self):
        return f'id: {str(self.id)}, pos: {self.pos}'
