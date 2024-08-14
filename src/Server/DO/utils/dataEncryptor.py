#!/usr/bin/python3
import numpy as np
import csv, sys

def encryptData(dataPath, outputPath, publicMetatadataEntity, doSecrets):
    plainData = []
    encryptedData = []
    with open(dataPath, "rt", newline='') as dataFile:
        fileReader = csv.reader(dataFile)
        for row in fileReader:
            plainData.append([float(row[_]) for _ in range(publicMetatadataEntity.d)])
    max_norm = float('-inf')
    interim_plaintext = []

    # Calculate interim pi matrix which is done with the use of secret_key, pis, w, and z.
    for pi in plainData:
        interim_pi = []
        norm_pi = np.linalg.norm(pi)
        # first len(pi) elements are s-2*p
        for index,p in enumerate(pi):
            interim_pi.append(doSecrets.secret_key[index] - 2*p)
        
        # add s + norm(p)**2
        interim_pi.append(doSecrets.secret_key[-1] + norm_pi**2)

        # add w
        interim_pi.extend(doSecrets.w)
        # add z
        interim_pi.extend(doSecrets.z)

        # Calculate maximum norm in pis
        max_norm = max(norm_pi, max_norm)
        interim_plaintext.append(interim_pi)
    
    # Calculate encrypted data matrix which is of (1+d+c+epsilon) X (1+d+c+epsilon) size.
    encryptedData = np.dot(interim_plaintext, np.linalg.inv(doSecrets.mbase))
    with open(outputPath, "w", newline='') as outputFile:
        csv.writer(outputFile).writerows(encryptedData)
    return max_norm

def decryptData(encryptedData, doSecrets, publicMetatadataEntity):
    decryptedData = []
    for data in encryptedData:
        decryptedData_temp = np.dot(data, doSecrets.mbase)
        decryptedData_final = []
        for index,val in enumerate(decryptedData_temp):
            if index < publicMetatadataEntity.d:
                decryptedData_final.append((doSecrets.secret_key[index] - val)/2)
            else:
                break
        decryptedData.append(decryptedData_final)
    return decryptedData