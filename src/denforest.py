def Core_Expiration_Time(p):
    return 2

def Insert(p):
    return
    # Insert p into the SpatialIndex

    # if |N'_eps(p)| >= tau then

def Connect(p, q):
    edge_ps.wgt = min(p.Ts, q.Ts)
    if(Connected(p,q)):
        edge_rs = FindMin(p,q)
        if(edge_rs.wgt < edge_ps.wgt):
            Cut(r,s)
            Link(p,q)
        return False
    else:
        Link(p,q)
        return True