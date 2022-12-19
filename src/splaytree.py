# check if x is root of the splay tree
def isRoot(x):
    if x.parent == None or (x.parent.left != x and x.parent.right != x):
        return True
    else:
        return False
    
def Rotate(x):
    p = x.parent
    
    if x == p.left:
        p.left = x.right
        x.right = p
        if p.left != None:
            p.left.parent = p
    else:
        p.right = x.left
        x.left = p
        if p.right != None:
            p.right.parent = p
    
    x.parent = p.parent
    p.parent = x
    
    if x.parent != None:
        if p == x.parent.left:
            x.parent.left = x
        elif p == x.parent.right:
            x.parent.right = x

# splay tree keeps frequentlly accessed nodes close to the top
def Splay(x):
    while isRoot(x) == False:
        p = x.parent
        if isRoot(p) == False:
            if (x == p.left) == (p == p.parent.left):
                Rotate(p)
            else:
                Rotate(x)
        
        Rotate(x)