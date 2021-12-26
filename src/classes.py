
class Node:
    def __init__(self, id:int, pos:tuple):
        self.id = id
        self.edge_in = {} # (src, w)
        self.edge_out = {} # (dest, w)
        self.tag = None
        self.dad =None
        self.pos = pos

# compare for priority queue in dijkstra
    def __lt__(self, other):
        return self.tag < other.tag





class PriorityQueue:
    def __init__(self):
        self.pq = []

    def enqueue(self, data):
        i = 0
        for curr in self.pq:
            if len(self.pq) == 0: self.pq.append(data
                                                 )
            if data < curr:
                i += 1
                continue
            else:
                self.pq.insert(i, data)
                break
        self.pq.append(data)

    def dequeue(self):
        return self.pq.pop()

    def is_empty(self):
        return len(self.pq) == 0
