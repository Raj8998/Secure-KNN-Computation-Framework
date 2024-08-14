#!/usr/bin/python3
import numpy as np

def performKnnOnEncryptedData(encryptedDataByUser, encryptedData, queryVector, k=3):
    distances = []
    for index,row in enumerate(encryptedDataByUser):
        distances.append((np.dot(row,queryVector),index))
    # print("performKnnOnEncryptedData: ", sorted(distances))
    distance = sorted(distances)[:k]
    knnResult = []
    for dist in distance:
        knnResult.append(encryptedData[dist[1]])
    return knnResult 