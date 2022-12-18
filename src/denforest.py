import lctree

# connect two points in the Link-Cut tree
def Connect(p, q, edgeTable):
    pqWeight = min(p.Tc, q.Tc)
    
    if lctree.Connected(p, q) == True:
        rs = lctree.FindMinE(p, q, edgeTable)
        
        # rs가 None일 수는 없음 Connected가 true이기 때문에
        
        if rs != None and rs.weight <= pqWeight:
            lctree.Cut(rs.n, rs.m, edgeTable)
            lctree.Link(p, q, edgeTable)
        
        # no merge
        return False
    else:
        lctree.Link(p, q, edgeTable)
        
        # potential merge
        return True