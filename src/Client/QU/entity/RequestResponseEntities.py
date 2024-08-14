#!/usr/bin/python3

class SimulateResponseEntity:
    def __init__(self, query, knn_response, knn_output_decrypted, knn_output_on_plaintext) -> None:
        self.query_vector = query
        self.knn_output = knn_response
        self.knn_output_decrypted = knn_output_decrypted
        if knn_output_on_plaintext != None:
            self.knn_output_on_plaintext = knn_output_on_plaintext

class queryEncryptRequestForDO:
    def __init__(self, query, userId) -> None:
        self.query = query
        self.userId = userId

class knnRequestForCSP:
    def __init__(self, query, userId, k) -> None:
        self.query = query
        self.userId = userId
        self.k = k

class sanityCheckRequest:
    def __init__(self, knnresults, query) -> None:
        self.knnresults = knnresults
        self.query = query