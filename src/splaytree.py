# check if x is root of the splay tree
def isRoot(x):
    if x.parent == None or (x.parent.left != x and x.parent.right != x):
        return True
    else:
        return False
    
# check if x is left child
def isLeft(x):
    if x == x.parent.left:
        return True
    else:
        return False

# for lazy propagation
def Push(x):
    if x.flip == 0:
        return
    
    x.flip = 0
    
    # swap left and right child
    temp = x.left
    x.left = x.right
    x.right = temp
    
    if x.left != None:
        x.left.flip ^= 1
    if x.right != None:
        x.right.flip ^= 1
    
def Rotate(x):
    if isLeft(x) == True:
        if x.right != None:
            x.right.parent = x.parent
        x.parent.left = x.right
        x.right = x.parent
    else:
        if x.left != None:
            x.left.parent = x.parent
        x.parent.right = x.left
        x.left = x.parent
        
    if isRoot(x.parent) == False:
        if isLeft(x.parent) == True:
            x.parent.parent.left = x
        else:
            x.parent.parent.right = x
    
    temp = x.parent
    x.parent = temp.parent
    temp.parent = x

# splay tree keeps frequentlly accessed nodes close to the top
def Splay(x):
    while isRoot(x) == False:
        if isRoot(x.parent) == False:
            Push(x.parent.parent)
            
        Push(x.parent)
        Push(x)
        
        if isRoot(x.parent) == True:
            continue
        
        if (x == x.parent.left) == (x.parent == x.parent.parent.left):
            Rotate(x.parent)
        else:
            Rotate(x)
        
        Rotate(x)
    
    Push(x)