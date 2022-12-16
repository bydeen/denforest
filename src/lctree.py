import splaytree

def SwitchPreferredChild(x, y):
    if x.right is not None:
        x.right.path_parent = x
    x.right = y
    if y is not None:
        y.parent = x
    
def Access(n):
    splaytree.splay(n)
    SwitchPreferredChild(n, None)
    if(n.path_parent is not None):
        m = n.path_parent
        splay(m)
        SwitchPreferredChild(m, n)
        Access(m)

def Link(n, m):
    Access(n)
    Access(m)
    n.left = main
    m.parent = n

def Cut(n, m):
    Access(n)

def Connected(n, m):
    return

def FindMin(n, m):
    return