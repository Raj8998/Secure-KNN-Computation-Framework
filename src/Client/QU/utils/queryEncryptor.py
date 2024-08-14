#!/usr/bin/python3
import numpy as np

def encryptQuery(query, quSecrets):
    return np.dot(quSecrets.beta1, np.dot(query, quSecrets.N_diagonal_matrix))

def decryptQuery(query, quSecrets):
    decryptedQuery = np.dot(query,np.linalg.inv(quSecrets.N_prime))
    return [np.sum(row) for row in decryptedQuery]