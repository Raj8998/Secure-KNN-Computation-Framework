#!/usr/bin/python3
class queryEncryptRequestForDO:
    def __init__(self, query, userId) -> None:
        self.query = query
        self.userId = userId

class queryEncryptResponseForDO:
    def __init__(self, encryptedQuery) -> None:
        self.encryptedQuery = encryptedQuery

class knnRequestForCSP:
    def __init__(self, query, userId, k) -> None:
        self.query = query
        self.userId = userId
        self.k = k

class UserBasedDataEncryptionRequestForCSP:
    def __init__(self, mt, userId) -> None:
        self.mt = mt
        self.userId = userId

class SanityCheckResponseEntity:
    def __init__(self, decryptedData, plainTextData) -> None:
        self.decryptedData = decryptedData
        self.plainTextData = plainTextData