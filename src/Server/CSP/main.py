#!/usr/bin/python3
import numpy as np
import os, csv, json
from entity.publicMetatadataEntity import PublicMetatadataEntity
from entity.CSPSecrets import CSPSecrets
from entity.RequestResponseEntities import *
from flask import Flask, request, jsonify
from utils.calculateKnn import *

app = Flask(__name__)

# Get the directory of the current script
script_directory = os.path.dirname(os.path.abspath(__file__))

# Get the project directory by going up one level
project_directory = os.path.dirname(script_directory)
encryptedDataPath = project_directory + "/Data/encrypted-data.csv"
publicVariablesFile = project_directory + "/../public-data.json"

publicMetatadataEntity = PublicMetatadataEntity(publicVariablesFile)
cspSecrets = CSPSecrets(encryptedDataPath, publicMetatadataEntity)
encryptedDataForUser = {}
# print(cspSecrets.encryptedData)

@app.route("/encryptDataBasedOnUser", methods=["POST"])
def encryptForUsers():
    # Get JSON data from the request
    json_data = request.get_json()

    if not json_data:
        return jsonify({'error': 'No JSON data received'}), 400
    
    Mt = np.array(json.loads(json_data["encryptDataBasedOnUser"])["mt"])
    userId = json.loads(json_data["encryptDataBasedOnUser"])["userId"]

    Mt_inv = np.linalg.inv(Mt)
    encryptedDataForUser[userId] = np.array(np.dot(cspSecrets.encryptedData,Mt_inv))
    return jsonify({'success': 'Data Encrypted'}), 200

@app.route("/findKnn", methods=["POST"])
def findKnn():
    # Get JSON data from the request
    json_data = request.get_json()

    if not json_data:
        return jsonify({'error': 'No JSON data received'}), 400
    
    query = json.loads(json_data["findknn"])["query"]
    userId = json.loads(json_data["findknn"])["userId"]
    k = json.loads(json_data["findknn"])["k"]

    # TODO: Perform KNN
    knnResult = performKnnOnEncryptedData(encryptedDataForUser[userId], cspSecrets.encryptedData, query, k)
    encryptedDataForUser.__delitem__(userId)

    return jsonify(knnResponseEntity(np.array(knnResult).tolist(), userId, k).__dict__)

if __name__ == "__main__":
    print("Starting CSP")
    app.run(host="0.0.0.0", port=8001, debug=True)