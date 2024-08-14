#!/usr/bin/python3
import numpy as np
import os, requests, json
from flask import Flask, request, jsonify
from entity.publicMetatadataEntity import PublicMetatadataEntity
from entity.QUSecrets import QUSecrets
from entity.RequestResponseEntities import *
from utils.queryEncryptor import *

app = Flask(__name__)

DOBaseUrl = "http://localhost:8002"
CSPBaseUrl = "http://localhost:8001"

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the project directory by going up one level
project_directory = os.path.dirname(script_directory)

publicVariablesFile = project_directory + "/../public-data.json"
publicMetadata = PublicMetatadataEntity(publicVariablesFile)
secrets = QUSecrets(publicMetadata)

def createDummyQuery():
    return [float("{:.2f}".format(np.random.rand()*publicMetadata.max_value)) for _ in range(publicMetadata.d)]

@app.route("/simulate", methods = ["GET"])
def simulateSecureNN():
    numberOfSimulations = request.args.get('count', default=1, type=int)
    verifyKnn = request.args.get('verify', default=False, type=bool)
    queryReponses = []
    for i in range(numberOfSimulations):
        # Create dummy query
        query = createDummyQuery()
        userId = np.random.randint(1,2000)

        # Encrypt the query on QU side
        encryptedQuery = encryptQuery(query, secrets)
        encryptedQueryArray = np.array(encryptedQuery).tolist()

        # Create queryEncryptionRequestObject to send to DO
        encryptRequestForDO = queryEncryptRequestForDO(encryptedQueryArray, userId)

        # Get DO encrypted query
        doQueryEncryptionResponse = requests.post(DOBaseUrl + "/encryptQuery", json={"encryptRequestForDO": json.dumps(encryptRequestForDO.__dict__)}, headers={'Content-Type': 'application/json'})
        if(doQueryEncryptionResponse.status_code == 200):
            encryptedQueryByDO = np.array(doQueryEncryptionResponse.json()["encryptedQuery"])

        # # Get the decrypted query
        decryptedQuery = decryptQuery(encryptedQueryByDO, secrets)

        # Create knnRequestObject to send to CSP
        findKnnRequestForCSP = knnRequestForCSP(np.array(decryptedQuery).tolist(), userId, publicMetadata.k)

        # Send the decrypted query to CSP to get the KNN results
        knnResultsResponse = requests.post(CSPBaseUrl + "/findKnn", json={"findknn": json.dumps(findKnnRequestForCSP.__dict__)}, headers={'Content-Type': 'application/json'})
        knnResults = ["No Results"]
        if(knnResultsResponse.status_code == 200):
            knnResults = np.array(knnResultsResponse.json()["knnResult"]).tolist()
        
        # Sanity Check
        sanityCheckRequestDTO = sanityCheckRequest(knnresults=knnResults, query=np.array(query).tolist())
        sanityCheckResponse = requests.post(DOBaseUrl + "/performSanityCheck", json={"sanityCheck": json.dumps(sanityCheckRequestDTO.__dict__)})
        decryptedData = np.array(sanityCheckResponse.json()["decryptedData"]).tolist()
        if verifyKnn:
            plainTextData = np.array(sanityCheckResponse.json()["plainTextData"]).tolist()
            queryResponseEntity = SimulateResponseEntity(query=query, knn_response=knnResults, knn_output_decrypted=decryptedData, knn_output_on_plaintext=plainTextData)
        else:
            queryResponseEntity = SimulateResponseEntity(query=query, knn_response=knnResults, knn_output_decrypted=decryptedData, knn_output_on_plaintext=None)
        queryReponses.append(queryResponseEntity)
    return jsonify([_.__dict__ for _ in queryReponses])




if __name__ == "__main__":
    print("Starting QU")
    app.run(host="0.0.0.0", port=8000, debug=True)