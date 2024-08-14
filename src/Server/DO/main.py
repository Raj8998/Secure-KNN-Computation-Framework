#!/usr/bin/python3
from utils.dataEncryptor import *
import numpy as np
import os, csv, json, requests
from entity.publicMetatadataEntity import PublicMetatadataEntity
from entity.DOSecrets import DOSecrets
from flask import Flask, request, jsonify
from entity.RequestResponseEntities import *
from utils.queryEncryptor import *
from utils.calculateKnnForSanity import *

app = Flask(__name__)

CSPBaseUrl = "http://localhost:8001"

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the project directory by going up one level
project_directory = os.path.dirname(script_directory)

dataPath = project_directory + "/DO/data/plain-data.csv"
encryptedDataPath = project_directory + "/Data/encrypted-data.csv"
publicVariablesFile = project_directory + "/../public-data.json"

publicMetatadataEntity = PublicMetatadataEntity(publicVariablesFile)
doSecrets = DOSecrets(publicMetatadataEntity)

def initializeDummyData():
    dummyData = [["{:.2f}".format(np.random.rand()*publicMetatadataEntity.max_value) for _ in range(publicMetatadataEntity.d)] for _ in range(publicMetatadataEntity.n)]
    with open(dataPath, "w", newline='') as dataFile:
        dataWriter = csv.writer(dataFile)
        dataWriter.writerows(dummyData)
    return

def main():
    initializeDummyData()
    global max_norm
    max_norm = encryptData(dataPath, encryptedDataPath, publicMetatadataEntity, doSecrets)
    return

@app.route("/encryptQuery", methods=["POST"])
def encryptQuery():
    # Get JSON data from the request
    json_data = request.get_json()

    if not json_data:
        return jsonify({'error': 'No JSON data received'}), 400
    
    encryptionRequest = queryEncryptRequestForDO(np.array(json.loads(json_data["encryptRequestForDO"])["query"]),json.loads(json_data["encryptRequestForDO"])["userId"])

    Mt, encryptedQuery = queryEncrypt(query=encryptionRequest.query, max_norm=max_norm, doSecrets=doSecrets, publicMetadata=publicMetatadataEntity)
    userBasedDataEncryptionRequestEntity = UserBasedDataEncryptionRequestForCSP(np.array(Mt).tolist(), encryptionRequest.userId)
    
    # Send above to CSP.
    userBasedDataEncryptionResponseFromCSP = requests.post(CSPBaseUrl + "/encryptDataBasedOnUser", json={"encryptDataBasedOnUser": json.dumps(userBasedDataEncryptionRequestEntity.__dict__)}, headers={'Content-Type': 'application/json'})

    # Create reqponse object and send back
    return jsonify(queryEncryptResponseForDO(np.array(encryptedQuery).tolist()).__dict__)

@app.route("/performSanityCheck", methods=["POST"])
def performSanityCheck():
    # Get JSON data from the request
    json_data = request.get_json()

    if not json_data:
        return jsonify({'error': 'No JSON data received'}), 400
    
    knnresults = json.loads(json_data["sanityCheck"])["knnresults"]
    query = json.loads(json_data["sanityCheck"])["query"]
    decryptedData = decryptData(knnresults, doSecrets, publicMetatadataEntity)

    plaintextData = []
    with open(dataPath, "r", newline='') as f:
            reader = csv.reader(f)
            for row in reader:
                floatData = [float(item) for item in row]
                plaintextData.append(floatData)
    knnResultForDecryptedText = performKnnOnPlainData(plaintextData, query, publicMetatadataEntity.k)

    sanityCheckResponseEntity = SanityCheckResponseEntity(decryptedData=np.array(decryptedData).tolist(), plainTextData=np.array(knnResultForDecryptedText).tolist())

    return jsonify(sanityCheckResponseEntity.__dict__)

if __name__ == "__main__":
    print("Starting DO")
    main()
    app.run(host="0.0.0.0", port=8002, debug=True)