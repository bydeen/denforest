import splaytree

class Node:
    def __init__(self, x, y, T):
        self.parent = None        
        self.left = None
        self.right = None

        self.x = x
        self.y = y
        self.T = T

        self.label = ''
        self.Tc = 0
    
class Edge:
    def __init__(self, n, m):
        self.n = n
        self.m = m
        self.weight = 0

# return smaller number
def min(a, b):
    if a < b:
        return a
    else:
        return b

# link n to link-cut tree's root with chain
def Access(n):
    splaytree.Splay(n)
    n.right = None
    while(n.parent != None):
        splaytree.Splay(n.parent)
        n.parent.right = n
        splaytree.Splay(n)

# link nodes n and m in different trees
def Link(n, m, edgeTable):
    Access(n)
    Access(m)
    m.left = n
    n.parent = m

    edge = Edge(n, m)
    edgeTable.update({(n, m):edge})
    edgeTable[n, m].weight = min(n.Tc, m.Tc)

# cut a link between nodes n and m
def Cut(n, m, edgeTable):
    Access(n)
    Access(m)
    m.left = None
    n.parent = None

# check if a path exists between nodes n and m
def Connected(n, m):
    if FindRoot(n) == FindRoot(m):
        return True
    else:
        return False

# find the root of the tree
def FindRoot(n):
    Access(n)
    while n.left != None:
        n = n.left
    splaytree.Splay(n)
    return n

# find the minimum weighted edge on the path between nodes n and m
def FindMinE(n, m, edgeTable):
    root = FindRoot(n) # store original root
    
    # make n a root node
    Access(n)
    splaytree.Splay(n)

    splaytree.Splay(m)
    m.right = None

    # initialize the minumum weighted edge
    if (m, m.parent) in edgeTable:
        e = edgeTable[m, m.parent]
    else:
        e = None

    # find the minimum weighted edge
    while(m.parent != None):
        if (m, m.parent) in edgeTable and (e == None or e.weight > edgeTable[m, m.parent].weight):
            e = edgeTable[m, m.parent]
        splaytree.Splay(m.parent)
        m.parent.right = m
        splaytree.Splay(m)

    # make original root a root node
    Access(root)
    splaytree.Splay(root)

    return e