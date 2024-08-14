#!/usr/bin/python3
import numpy as np

def queryEncrypt(query, max_norm, doSecrets, publicMetadata):
    qmax = np.max(query)
    Mt = [[np.random.uniform(qmax, 2*qmax) for _ in range(doSecrets.eta)] for _ in range(doSecrets.eta)]
    for i in range(doSecrets.eta):
        for j in range(doSecrets.eta):
            if i == j:
                Mt[i][j] = np.random.uniform(max_norm, 2*max_norm)

    Msec = np.dot(Mt,doSecrets.mbase)
    query_matrix = np.diag(np.concatenate([query, [1], doSecrets.x, doSecrets.zero]))
    error_vector = np.random.uniform(qmax, 2*qmax, (doSecrets.eta,doSecrets.eta))

    encryptedQuery = np.dot(doSecrets.beta2, (np.dot(Msec, query_matrix) + error_vector))
    return Mt, encryptedQuery