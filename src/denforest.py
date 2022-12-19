import matplotlib.pyplot as plt
import lctree

# connect two points in the Link-Cut tree
def Connect(p, q, edgeTable):
    pqWeight = min(p.Tc, q.Tc)
    
    if lctree.Connected(p, q) == True:
        rs = lctree.FindMinE(p, q, edgeTable)
        
        if rs.weight <= pqWeight:
            lctree.Cut(rs.n, rs.m, edgeTable)
            lctree.Link(p, q, edgeTable)
        
        # no merge
        return False
    else:
        lctree.Link(p, q, edgeTable)
        
        # potential merge
        return True
    
def Result(name, nodeTable):
    # Clustering Result Print Labels
    # for d in nodeTable:
    #     print(d, nodeTable[d].label)

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
            
    x1, y1 = zip(*cTable.keys())
    x2, y2 = zip(*bTable.keys())
    x3, y3 = zip(*nTable.keys())

    plt.scatter(x1, y1, color='red', s=3)
    plt.scatter(x2, y2, s=3)
    plt.scatter(x3, y3, color='grey', s=3)

    plt.show()
    filepath = './results/' + str(name)
    plt.savefig(name)