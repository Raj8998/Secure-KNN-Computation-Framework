#!/usr/bin/python3
import numpy as np
class QUSecrets:
    def __init__(self, publicMetadata) -> None:
        self.eta = publicMetadata.d + publicMetadata.c + publicMetadata.epsilon + 1

        self.beta1 = float("{:.2f}".format(np.random.rand()))

        self.N_diagonal_matrix = [[0.00 for _ in range(publicMetadata.d)] for _ in range(publicMetadata.d)]
        for i in range(publicMetadata.d):
            for j in range(publicMetadata.d):
                if i == j:
                    self.N_diagonal_matrix[i][j] = float("{:.2f}".format(np.random.rand()*publicMetadata.max_value))
        
        self.N_prime = np.diag(np.concatenate([np.diag(self.N_diagonal_matrix), np.ones(self.eta-publicMetadata.d)]))