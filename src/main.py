import sys
import math
import numpy as np

import denforest
import lctree

# Input data is in format (x, y) and sorted in time order
# Use count-based window
# The data points in the same stride are processed together
inputFile = sys.argv[1]
tau = int(sys.argv[2])
eps = float(sys.argv[3])
window = int(sys.argv[4])
stride = int(sys.argv[5])

data = np.loadtxt(open(inputFile), delimiter=",") # dataset

# set the time to zero
currentTime = 0

# hash table for nostalgic cores, {Tc : Node p}
ncoreTable = {}

# hash table for DenTree
nodeTable = {} # contains all the data points in the window, (x, y) as key
edgeTable = {} # contains all the edges in the DenTree, Node n as key, (Node m, edge weight) as value

for i in range(0, int(len(data) / stride)):
    print('Stride', currentTime + 1, 'Processing')
    
    # New data points in the same stride
    spts = data[i * stride:(i + 1) * stride]

    # add timestamp for each data points
    spts = np.insert(spts, 2, currentTime, axis=1)

    # add to the nodeTable
    for p in spts:
        newNode = lctree.Node(p[0], p[1], currentTime)
        nodeTable.update({(p[0], p[1]):newNode})
        
    # Insert
    for p in spts:
        pcoord = (p[0], p[1]) # coordinates
        pnode = nodeTable[pcoord] # node in DenTree
        
        # STEP 1: Point Classification
        # make NepsPrev set
        NepsPrev = {}
        for d in nodeTable:
            
            # calculate the distance between two points p and d
            dist = math.dist(pcoord, d)
            
            # if d is a eps-neighbor, add it to the NepsPrev
            if pcoord != d and dist <= eps:
                NepsPrev.update({d:nodeTable[d]})
        
        # if p is a nostalgic core
        if len(NepsPrev) >= tau:
            mst = 0
            
            # STEP 2: Determination of Core-expiration Time
            # Python dictionary preserves the insertion order
            # q is a point such that its timestamp q.T is the tau-th largest, p.Tc = q.T + |W|
            Tc = int(list(NepsPrev.values())[len(NepsPrev) - tau].T + window / stride)
            pnode.Tc = Tc
            pnode.label = 'ncore'

            # add p to the ncoreTable
            # ncoreTable can have multiple node values for one key
            if Tc in ncoreTable:
                ncoreTable[Tc].append(pnode)
            else:
                ncoreTable.update({Tc:[pnode]})

            for key in ncoreTable:
                narray = ncoreTable[key]
                
                for n in narray:
                    if pnode != n and (n.x, n.y) in NepsPrev:
                        if key >= currentTime and denforest.Connect(pnode, nodeTable[n.x, n.y], edgeTable):
                            mst += 1
                
            # determine the type of cluster evolution by the mst value
            if mst == 0:
                evolType = 'emerges'
            elif mst == 1:
                evolType = 'expands'
            else:
                evolType = 'merged'
                
        # STEP 4: Updating Borders
        if pnode.label == 'ncore':
            for d in NepsPrev:
                dnode = nodeTable[d[0], d[1]]
                
                if dnode.label == 'border':
                    if pnode.Tc > dnode.Tc:
                        dnode.Tc = pnode.Tc
                elif dnode.label == '' or dnode.label == 'noise':
                    dnode.label = 'border'
        else:
            for d in NepsPrev:
                dnode = nodeTable[d[0], d[1]]
                
                if dnode.label == 'ncore':
                    pnode.label = 'border'
                    if pnode.Tc > dnode.Tc:
                        dnode.Tc = pnode.Tc

        if pnode.label == '':
            pnode.label = 'noise'
            
    # Delete
    if(i * stride >= window):
        
        # Outdated data points in the stride
        spts = data[(i * stride) - window:(i + 1) * stride - window]
        
        # STEP 1: Finding Expiring Nostalgic Cores
        Eq = [] # set of ncores expired by the deletion of q
        if ncoreTable.get(currentTime) != None:
            Eq = ncoreTable[currentTime]
            del ncoreTable[currentTime]
        
        for x in Eq:
            L = [] # set of ncores linked to x
            
            if edgeTable.get(x) != None:
                for edge in edgeTable[x]:
                    if edge.m.label == 'ncore':
                        L.append(edge.m)

            # STEP 2: Cutting Links from MSTs
            if len(L) == 0:
                evolType = 'dissipates'
            elif len(L) == 1:
                evolType = 'shrinks'
            else:
                evoltype = 'split'
                
            for y in L:
                lctree.Cut(x, y, edgeTable)

            # Reclassify x as either border or noise by the |L| value
            if len(L) >= 1:
                x.label = 'border'
            else:
                x.label = 'noise'
            
        for q in spts:
            nodeTable.pop((q[0], q[1]), 'already deleted')
    
    currentTime += 1

denforest.Result('result', nodeTable)