#!/usr/bin/pyhton3
import csv

class CSPSecrets:
    def __init__(self, encryptedDataPath, publicMetadata) -> None:
        self.eta = publicMetadata.d + publicMetadata.c + publicMetadata.epsilon + 1

        encryptedData = []
        with open(encryptedDataPath, "r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                floatData = [float(item) for item in row]
                encryptedData.append(floatData)
        self.encryptedData = encryptedData