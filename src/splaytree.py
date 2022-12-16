class Node:
    def __init__(self, data):
        self.left = None
        self.right = None
        self.parent = None

        self.data = data
        self.path_parent = None

# check if x is root of the splay tree
def isRoot(x):
    if x.parent is None or (x.parent.left != x and x.parent.right != x):
        return True
    else:
        return False

def leftRotate(x):
    y = x.right
    if y is not None:
        x.right = y.left
        if y.left is not None:
            y.left.parent = x
        y.parent = x.parent

    if x.parent is None:
        root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    
    if y is not None:
        y.left = x
    x.parent = y

def rightRotate(x):
    y = x.left
    if y is not None:
        x.left = y.right
        if y.right is not None:
            y.right.parent = x
        y.parent = x.parent

    if x.parent is None:
        root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    
    if y is not None:
        y.right = x
    x.parent = y

def splay(x):
    while x.parent is not None:
        if x.parent.parent is None:
            if x.parent.left == x:
                right_rotate(x.parent)
            else:
                left_rotate(x.parent)
        elif x.parent.left == x and x.parent.parent.left == x.parent:
            right_rotate(x.parent.parent)
            right_rotate(x.parent)
        elif x.parent.right == x and x.parent.parent.right == x.parent:
            left_rotate(x.parent.parent)
            left_rotate(x.parent)
        elif x.parent.left == x and x.parent.parent.right == x.parent:
            right_rotate(x.parent)
            left_rotate(x.parent)
        else:
            left_rotate(x.parent)
            right_rotate(x.parent)