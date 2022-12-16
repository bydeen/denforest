# check if x is root of the splay tree
def isRoot(x):
    if x.parent == None or (x.parent.left != x and x.parent.right != x):
        return True
    else:
        return False        

def leftRotate(x):
    y = x.right
    if y != None:
        x.right = y.left
        if y.left != None:
            y.left.parent = x
        y.parent = x.parent

    if x.parent == None:
        root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    
    if y != None:
        y.left = x
    x.parent = y

def rightRotate(x):
    y = x.left
    if y != None:
        x.left = y.right
        if y.right != None:
            y.right.parent = x
        y.parent = x.parent

    if x.parent == None:
        root = y
    elif x == x.parent.left:
        x.parent.left = y
    else:
        x.parent.right = y
    
    if y != None:
        y.right = x
    x.parent = y

# moves x to the root node
def Splay(x):
    while isRoot(x) == False:
        if isRoot(x.parent) == True:
            # zig
            if x.parent.left == x:
                rightRotate(x.parent)
            # zag
            else:
                leftRotate(x.parent)
        # zigzig
        elif x.parent.left == x and x.parent.parent.left == x.parent:
            rightRotate(x.parent.parent)
            rightRotate(x.parent)
        # zagzag
        elif x.parent.right == x and x.parent.parent.right == x.parent:
            leftRotate(x.parent.parent)
            leftRotate(x.parent)
        # zigzag
        elif x.parent.left == x and x.parent.parent.right == x.parent:
            rightRotate(x.parent)
            leftRotate(x.parent)
        # zagzig
        else:
            leftRotate(x.parent)
            rightRotate(x.parent)