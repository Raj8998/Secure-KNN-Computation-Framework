#!/usr/bin/python3
class knnResponseEntity:
    def __init__(self, knnResult, userId, k) -> None:
        self.knnResult = knnResult
        self.userId = userId
        self.k = k