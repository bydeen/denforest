import lctree

# connect two points in the Link-Cut tree
def Connect(p, q, edgeTable):
    pqWeight = min(p.Tc, q.Tc)
    
    if lctree.Connected(p, q) == True:
        rs = lctree.FindMinE(p, q, edgeTable)
        
        if rs != None and rs.weight <= pqWeight:
            lctree.Cut(rs.n, rs.m, edgeTable)
            lctree.Link(p, q, edgeTable)
        
        return False
    else:
        lctree.Link(p, q, edgeTable)
        return True