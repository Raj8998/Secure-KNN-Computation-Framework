#!/usr/bin/python3
import math

def performKnnOnPlainData(data_matrix,query,k=3):
    distance=[]
    for index,data_row in enumerate(data_matrix):
        euclidean_distance = 0
        for i in range(len(data_row)):
 
            #calculate the euclidean distance of p from training points 
            euclidean_distance = euclidean_distance + (data_row[i]-query[i])**2
 
        distance.append((math.sqrt(euclidean_distance), index))
 
    # sort the distance list in ascending order
    # and select first k distances
    # print("performKnnOnPlainData:",sorted(distance))
    distance = sorted(distance)[:k]
    knnResult = []
    for dist in distance:
        knnResult.append(data_matrix[dist[1]])
    return knnResult