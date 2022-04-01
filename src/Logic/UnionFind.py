class UNode:
    def __init__(self, value, parent=None):
        self.value = value
        if parent is not None:
            self.parent = parent
        else:
            self.parent = self
        self.rank = 0

    def __str__(self):
        return self.value


class UnionFind:
    def __init__(self):
        self.nodes = {}  # dict of all the nodes in the struct {val:node}
        self.sets = []  # list of all the representative

    def make_set(self, value):
        node = UNode(value)
        self.sets.append(node)
        self.nodes[value] = node

    def find(self, val):
        node = self.nodes[val]
        if node.parent == node:
            return node
        else:
            return self.find(node.parent.value)

    def union(self, val1, val2):
        parent1 = self.find(val1)
        parent2 = self.find(val2)
        if parent1 == parent2:
            return
        if parent1.rank < parent2.rank:
            parent1.parent = parent2
            self.sets.remove(parent1)

        elif parent1.rank > parent2.rank:
            parent2.parent = parent1
            self.sets.remove(parent2)

        else:
            parent2.parent = parent1
            self.sets.remove(parent2)
            parent1.rank += 1

    def __str__(self):
        ans = ''
        for val, node in self.nodes.items():
            ans += f'\nparent: {self.find(val).__str__()}, node: {node.__str__()}'

        return ans

if __name__ == '__main__':
    union = UnionFind()
    union.make_set(1)
    union.make_set(2)
    union.make_set(3)
    union.make_set(4)
    union.make_set(5)
    union.make_set(6)
    print(union)
    union.union(6, 5)
    print(union)




