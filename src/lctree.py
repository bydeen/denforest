import splaytree

class Node:
    def __init__(self, data):
        self.parent = None        
        self.left = None
        self.right = None
        self.data = data

# link n to link-cut tree's root with chain
def Access(n):
    splaytree.Splay(n)
    n.right = None
    while(n.parent != None):
        splaytree.Splay(n.parent)
        n.parent.right = n
        splaytree.Splay(n)

# link nodes n and m in different trees
def Link(n, m):
    Access(n)
    Access(m)
    m.left = n
    n.parent = m

# cut a link between nodes n and m
def Cut(n, m):
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
def FindMinE(n, m):
    return True