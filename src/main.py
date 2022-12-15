import csv
import sys
import time
import math
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import geopandas as gpd

import denforest
import lctree

# Input data is in format (x, y, timestamps) and sorted in time order
# Use count-based window
# The data points in the same stride are processed together

# ex) python3.8 main.py ./input.csv 5 0.2 100 10
inputFile = sys.argv[1]
tau = int(sys.argv[2])
eps = float(sys.argv[3])
window = int(sys.argv[4])
stride = int(sys.argv[5])

# dtype = np.dtype([("x", float), ("y", float), ("time", int)])
# data = np.loadtxt(open(inputFile), dtype=dtype, delimiter=",", usecols=(0, 1, 2)) # dataset

data = np.loadtxt(open(inputFile), delimiter=",") # dataset
# wpts = np.empty([0, 2], dtype=float) # data points in the window
wpts = ([0, 0, 0])
# spts = np.zeros([stride, 3], dtype=float) # data points in the same stride

ncore = {}

# for currentTime in range(0, int(data[-1][2]) + 1):
# for currentTime in range(0, 2):

    # data points in the same stride
    # rows = np.where(data["time"] == currentTime)
    # spts = data[rows]
    # print(spts)

# start time set to zero
currentTime = 0

# hash table for n-cores
ncoreTable = {}

for i in range(0, int(len(data) / stride)):
    
    # data points in the same stride
    spts = data[i * stride:(i + 1) * stride]

    # add timestamp for each data points
    spts = np.insert(spts, 2, currentTime, axis=1)
    print(spts)

    # insert data points into the window (wpts)
    if i == 0:
        wpts = spts
    else:
        wpts = np.vstack((wpts, spts))

    # Insert
    for p in spts:
        # insert p into the SpatialIndex
        
        # STEP 1: Point Classification
        # make N_eps_prev set
        N_eps_prev = np.empty([0, 3])
        for d in wpts:
            dist = math.dist(p, d)
            # print(dist)
            if np.array_equal(p, d) == False and dist <= eps:
                N_eps_prev = np.vstack((N_eps_prev, d))
        
        # if p is nostalgic core
        if len(N_eps_prev) >= tau:
            mst = 0
            # STEP 2: Determination of Core-expiration Time
            # sort the eps-neighbors in the order of timestamps
            sorted_N_eps_prev = N_eps_prev[N_eps_prev[:,2].argsort()]

            # q is a point such that its timestamp q.T is the tau-th largest
            # p.Tc = q.T + |W|
            expT = sorted_N_eps_prev[tau - 1][2] + window

            ncoreTable.update({"x": p[0], "y": p[1], "Tc": int(expT)})
            print(ncoreTable)

            for n in N_eps_prev:
                # TODO: if n is n-core
                if n[2] >= currentTime and Connet(p, n):
                    mst += 1

            # determine the type of cluster evolution by the mst value
            if mst == 0:
                evol_type = "emerges"
            elif mst == 1:
                evol_type = "expands"
            else:
                evol_type = "merged"

        # STEP 4: Updating Borders

    # Delete

    currentTime += 1


    # if currentTime == 0:
    #     wpts = spts
    # else:
    #     wpts = np.concatenate((wpts, spts), axis=0)

    # # print(wpts)

    # for p in spts:
    #     N_eps_prev_num = 0
    #     for d in wpts:
    #         dist = math.dist((p[0], p[1]), (d[0], d[1]))
    #         if d != p and dist <= eps:
    #             N_eps_prev_num += 1
        
    #     if N_eps_prev_num >= tau: # process the nostalgic core

    #         mst = 0
    #         ncore["x"] = p[0]
    #         ncore["y"] = p[1]
    #         ncore["T_c"] = denforest.Core_Expiration_Time(p)

    #         # for n in N_eps_prev:
    #             # if n.T_c >= currentTime and Connect(p, n):
    #                 # mst += 1
            
            # # determine the type of cluster evolution by the mst value
            # if mst == 0:
            #     evol_type = "emerge"
            # elif mst == 1:
            #     evol_type = "expand"
            # else:
            #     evol_type = "merged"
                
        # process the noise/borders


        # if()
        # denforest.Insert(p)
        # print(type(p))

    # rows = np.where(t[:,3] == 'bar')
    # result = t1[rows]

    # print(result)

#   wpts = np.vstack( (wpts, data[i * stride : (i + 1) * stride]) ) # data points inserted into the window
  
#   # insert p into the SpatialIndex
  
#   for j in range(0, stride): # for each inserted point p
    
#     idx = i * stride + j

#     spts[j][0] = data[idx][0] # x-coordinate value
#     spts[j][1] = data[idx][1] # y-coordinate value

#     num = 0

#     n_eps = np.empty([0, 2], dtype=float)

#     for k in range(0, len(wpts)):
#       dist = np.linalg.norm(spts[j][0:1] - wpts[k])
#       if(dist <= eps):
#         n_eps = np.stack( (n_eps, wpts[k]) )
#         num += 1
#         if wpts[k][2] >= currentTime and Connect:
#           mst += 1

#     # Determine the type of cluster evolution by the mst value
    
#     # Process the noise/borders
#     if(num >= tau):
#       mst = 0

#   currentTime += 1

#   x, y = wpts.T
#   # plt.scatter(x, y)
#   # plt.pause(0.5)
#   # plt.show()
