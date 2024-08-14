# Structure of the Project
- There are 3 microservices mimicing Query Users(QU), Data Owner(DO) and Cloud Service Provider(CSP) for which code is available respectively in "Client/QU", "Server/DO" and "Server/CSP" folders.
- The "Server/DO/Data" folder contains data in plaintext form and the "Server/Data" folder contains encrypted data which is being initialized by DO on every instance of its run.
- The "public-data.json" file contains public variables which are described as below:
    1. "n": Number of data vectors (Rows in data-matrix)
    2. "d": Dimension of data vectors (columns in data matrix)
    3. "c", and "epsilon": values expected by the algorithm to calculate "eta = d + 1 + c + epsilon"
    4. "max_value": Maximum value a data point can achieve
    5. "k": input parameter value for K-NN Algorithm

# How to start the application
- Step-1: Start DO by running command "python3 -B Server/DO/main.py" (adjust the command according to your need)
- Step-2: Start CSP by running command "python3 -B Server/CSP/main.py" (adjust the command according to your need)
- Step-3: Start QU by running command "python3 -B Server/QU/main.py" (adjust the command according to your need)
- Now you can access the QU's "/simulate" API which will simulate the entire process by hitting "http://localhost:8000/simulate" in your browser. (The eimulation of entire process can take upto 10-15 seconds)
**NOTE:** The steps given above MUST be followed in sequence.

# Flexible Features
- You can change the "public-data.json" file to your needs and if your application was already running then restart your application following the steps provided above.
- The "/simulate" API has 2 GET parameters:
    - "count": This will indicate how many times you want to simulate the process. count=3 means, 3 different queries will be run on same data points. Default value of count is 1
    - "verify": This is a boolean expecting "True" for "False" as input. verify=True means that the simulator will also try to apply K-NN algorithm on plaintext data, and plaintext queries and give output for user to verify it.