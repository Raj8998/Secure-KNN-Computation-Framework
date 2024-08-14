#!/usr/bin/python3
import json

class PublicMetatadataEntity:
    def __init__(self, publicVariableFile) -> None:
        with open(publicVariableFile, "rt") as f:
            publicData = json.loads(f.read())
        self.d = publicData["d"]
        self.c = publicData["c"]
        self.n = publicData["n"]
        self.k = publicData["k"]
        self.epsilon = publicData["epsilon"]
        self.max_value = publicData["max_value"]