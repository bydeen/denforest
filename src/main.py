import sys
import math
import numpy as np
import matplotlib.pyplot as plt
# import pandas as pd
# import geopandas as gpd

import denforest
import lctree

# Input data is in format (x, y, timestamps) and sorted in time order
# Use count-based window
# The data points in the same stride are processed together

# ex) python3.8 main.py ../dataset/input.csv 5 1.5 100 10
inputFile = sys.argv[1]
# inputFile = '../dataset/input.csv'
tau = int(sys.argv[2])
# tau = 5
eps = float(sys.argv[3])
# eps = 0.1
window = int(sys.argv[4])
# window = 100
stride = int(sys.argv[5])
# stride = 10

data = np.loadtxt(open(inputFile), delimiter=",") # dataset

# start time set to zero
currentTime = 0

# hash table for n-cores, Tc as a key
ncoreTable = {}

# hash table for DenTree
nodeTable = {} # contains all the data points in the window, (x, y) as key
edgeTable = {} # contains all the edges in the DenTree, (Node n, Node m) as key

for i in range(0, int(len(data) / stride)):
    
    # data points in the same stride
    spts = data[i * stride:(i + 1) * stride]

    # add timestamp for each data points
    spts = np.insert(spts, 2, currentTime, axis=1)

    # add to nodeTable, delete when doing deletion
    for p in spts:
        newNode = lctree.Node(p[0], p[1], currentTime)
        nodeTable.update({(p[0], p[1]):newNode})

    # insert data points into the window (wpts)
    if i == 0:
        wpts = spts
    else:
        wpts = np.vstack((wpts, spts))

    # Insert
    for p in spts:

        # STEP 1: Point Classification
        # make N_eps_prev set
        N_eps_prev = np.empty([0, 3])
        for d in wpts:
            dist = math.dist(p[:2], d[:2])
            if p is not d and dist <= eps:
                N_eps_prev = np.vstack((N_eps_prev, d))
        
        # if p is nostalgic core
        # if len(N_eps_prev) >= tau:
        if len(N_eps_prev) > tau:
            mst = 0
            # STEP 2: Determination of Core-expiration Time
            # sort the eps-neighbors in the order of timestamps
            sorted_N_eps_prev = N_eps_prev[N_eps_prev[:,2].argsort()]

            # q is a point such that its timestamp q.T is the tau-th largest
            # p.Tc = q.T + |W|
            Tc = int(sorted_N_eps_prev[tau - 1][2] + window)
            nodeTable[p[0], p[1]].Tc = Tc
            nodeTable[p[0], p[1]].label = 'ncore'

            # hashmap with core-expiration time as key and (x, y, T) as value
            ncoreTable.update({Tc:p})

            for key in ncoreTable:
                n = ncoreTable[key]

                if p is not n and n in N_eps_prev:
                    # if key >= currentTime and denforest.Connect(p, n):
                    if key >= currentTime and denforest.Connect(nodeTable[p[0], p[1]], nodeTable[n[0], n[1]], edgeTable):
                        mst += 1
                
            # determine the type of cluster evolution by the mst value
            if mst == 0:
                evolType = 'emerge'
                # print('Cluster Emerges')
            elif mst == 1:
                evolType = 'expand'
                # print('Cluster Expands')
            else:
                evolType = 'merged'
                # print('Cluster Merged')
            
        # STEP 4: Updating Borders
        flag = False

        if nodeTable[p[0], p[1]].label == 'ncore':
            flag = True
            for d in N_eps_prev:
                if nodeTable[d[0], d[1]].label == 'border':
                    if nodeTable[p[0], p[1]].Tc > nodeTable[d[0], d[1]].Tc:
                        nodeTable[d[0], d[1]].Tc = nodeTable[p[0], p[1]].Tc
                elif nodeTable[d[0], d[1]].label == '' or nodeTable[d[0], d[1]].label == 'noise':
                    nodeTable[d[0], d[1]].label = 'border'
        else:
            for d in N_eps_prev:
                if nodeTable[d[0], d[1]].label == 'ncore':
                    nodeTable[p[0], p[1]].label = 'border'
                    if nodeTable[p[0], p[1]].Tc > nodeTable[d[0], d[1]].Tc:
                        nodeTable[p[0], p[1]].Tc = nodeTable[d[0], d[1]].Tc
                    flag = True

        if flag == False:
            nodeTable[p[0], p[1]].label = 'noise'

    # TODO: Delete

    currentTime += 1

# Clustering Result Print Labels
# for d in nodeTable:
#     print(d, nodeTable[d].label)


# Clustering Result Visualization
# cTable = {} # ncore
# bTable = {} # border
# nTable = {} # noise

# for d in nodeTable:
#     if nodeTable[d].label == 'ncore':
#         print('ncore')
#         cTable.update({d:nodeTable[d]})
#     elif nodeTable[d].label == 'border':
#         bTable.update({d:nodeTable[d]})
#     else:
#         nTable.update({d:nodeTable[d]})
        
# x1, y1 = zip(*cTable.keys())
# x2, y2 = zip(*bTable.keys())
# x3, y3 = zip(*nTable.keys())

# plt.scatter(x1, y1, color='red', s=3)
# plt.scatter(x2, y2, s=3)
# plt.scatter(x3, y3, color='grey', s=3)

# plt.show()