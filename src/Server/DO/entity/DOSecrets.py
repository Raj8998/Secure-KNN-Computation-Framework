#!/usr/bin/python3
import numpy as np

class DOSecrets:
    def __init__(self, publicMetadata) -> None:
        self.eta = publicMetadata.d + publicMetadata.c + publicMetadata.epsilon + 1
        # Sample base secret matrix Mbase
        self.mbase = np.random.rand(int(self.eta), int(self.eta))

        # Generate long-term secret vector s
        self.secret_key = [float("{:.2f}".format(np.random.rand()*publicMetadata.max_value)) for _ in range(publicMetadata.d + 1)]

        # Generate fixed vector w for each data vector
        self.w = [float("{:.2f}".format(np.random.rand()*publicMetadata.max_value)) for _ in range(publicMetadata.c)]

        # Generate fixed vector x for query vector
        self.x = [float("{:.2f}".format(np.random.rand()*publicMetadata.max_value)) for _ in range(publicMetadata.c)]

        # Sample ephemeral secret vector z
        self.z = [float("{:.2f}".format(np.random.rand()*publicMetadata.max_value)) for _ in range(publicMetadata.epsilon)]

        # Sample zero vector
        self.zero = [0.00 for _ in range(publicMetadata.epsilon)]

        # beta2 for query encryption
        self.beta2 = float("{:.2f}".format(np.random.rand()))