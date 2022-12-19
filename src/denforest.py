import matplotlib.pyplot as plt
import lctree

# connect two points in the Link-Cut tree
def Connect(p, q, edgeTable):
    pqWeight = min(p.Tc, q.Tc)
    
    if lctree.Connected(p, q) == True:
        rs = lctree.FindMinE(p, q, edgeTable)
        
        if rs != None and rs.weight <= pqWeight:
            lctree.Cut(rs.n, rs.m, edgeTable)
            lctree.Link(p, q, edgeTable)
        
        # no merge
        return False
    else:
        lctree.Link(p, q, edgeTable)
        
        # potential merge
        return True
    
def Result(name, nodeTable):
    # Clustering Result Visualization
    cTable = {} # ncore
    bTable = {} # border
    nTable = {} # noise

    for d in nodeTable:
        if nodeTable[d].label == 'ncore':
            cTable.update({d:nodeTable[d]})
        elif nodeTable[d].label == 'border':
            bTable.update({d:nodeTable[d]})
        else:
            nTable.update({d:nodeTable[d]})
            
    xcore, ycore = zip(*cTable.keys())
    xborder, yborder = zip(*bTable.keys())
    xnoise, ynoise = zip(*nTable.keys())

    plt.scatter(xnoise, ynoise, color='grey', s=2)
    plt.scatter(xborder, yborder, color='C0', s=2)
    plt.scatter(xcore, ycore, color='red', s=2)

    plt.show()
    plt.savefig(name)