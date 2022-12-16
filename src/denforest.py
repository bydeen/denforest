def Connect(p, q):
    edge_pq.wgt = min(p.Ts, q.Ts)
    if(Connected(p,q)):
        edge_rs = FindMin(p,q)
        if(edge_rs.wgt < edge_pq.wgt):
            Cut(r,s)
            Link(p,q)
        return False
    else:
        Link(p,q)
        return True