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

# link n to link-cut tree's root with chain
def Access(n):
    splaytree.Splay(n)
    n.right = None
    while n.parent != None:
        splaytree.Splay(n.parent)
        n.parent.right = n
        if n.parent != None:
            splaytree.Splay(n)

# link nodes n and m in different trees
def Link(n, m, edgeTable):
    Access(m)
    Access(n)
    m.left = n
    n.parent = m

    # add edge n to m to the edgeTable
    edge1 = Edge(n, m)
    edge1.weight = min(n.Tc, m.Tc)
    
    if n in edgeTable:
        edgeTable[n].append(edge1)
    else:
        edgeTable.update({n:[edge1]})
    
    # add edge m to n to the edgeTable
    edge2 = Edge(m, n)
    edge2.weight = min(m.Tc, n.Tc)
    
    if m in edgeTable:
        edgeTable[m].append(edge2)
    else:
        edgeTable.update({m:[edge2]})

# cut a link between nodes n and m
def Cut(n, m, edgeTable):
    Access(n)
    Access(m)
    m.left = None
    n.parent = None
    
    # delete edge n to m from the edge table
    if edgeTable.get(n) != None: # TODO
        for edge in edgeTable[n]:
            if edge.n == n:
                edgeTable[n].remove(edge)
                    
        if not edgeTable[n]:
            edgeTable.pop(n)
    
    # delete edge m to n from the edge table
    if edgeTable.get(m) != None: # TODO
        for edge in edgeTable[m]:
            if edge.n == m:
                edgeTable[m].remove(edge)
                
        if not edgeTable[m]:
            edgeTable.pop(m)

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
    
    # chain the path between n and m
    Access(m)
    
    # initialize the minimum weight of edges
    for edge in edgeTable[n]:
        # print(n.parent)
        if edge.m == n.parent:
            minEdge = edge
            minWeight = edge.weight
    
    # print(minEdge, minWeight)
            
    # minWeight = edgeTable[n]
    # print(edgeTable[n])
    # while n != m:
    #     for edge in edgeTable[n]:
    #         minWeight = edge.n
            
    #         n = n.parent
        
        
    # # initialize the minumum weighted edge
    # if (m, m.parent) in edgeTable: # TODO
    #     e = edgeTable[m, m.parent]
    # else:
    #     e = None

    # # find the minimum weighted edge
    # while(m.parent != None):

    #     # TODO
    #     if (m, m.parent) in edgeTable and (e == None or e.weight > edgeTable[m, m.parent].weight):
    #         e = edgeTable[m, m.parent]
    #     splaytree.Splay(m.parent)
    #     m.parent.right = m
    #     splaytree.Splay(m)

    splaytree.Splay(n)
    
    # make original root a root node
    Access(root)
    splaytree.Splay(root)

    return minEdge

edgeTable = {}
n1 = Node(1, 2, 3)
n2 = Node(2, 1, 3)
n3 = Node(3, 2, 3)
n4 = Node(4, 2, 3)

Link(n1, n2, edgeTable)
Link(n1, n3, edgeTable)
Link(n2, n4, edgeTable)

# root = FindRoot(n1) # store original root

print(n1.parent.x)
print(n1.left, n1.right)

print(n2.parent.x)
print(n2.left.x, n2.right)

print(n3.parent.x)
print(n3.left, n3.right)

print(n4.parent)
print(n4.left.x, n4.right)

print(FindRoot(n1).x, FindRoot(n2).x, FindRoot(n3).x, FindRoot(n4).x)
# print(n1.left)
# make n a root node
# print(n2.parent)
Access(n1)
# splaytree.Splay(n2)
# print(n2.parent)

# chain the path between n and m
Access(n4)

# print(n1.parent.x, n1.parent.y)