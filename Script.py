import time
import pymongo
import json

from github import Github
from pymongo import MongoClient

ACCESS_TOKEN="INSERT HERE YOUR ACCESS TOKEN"
CONNECTION_TO_MONGO = "INSERT HERE YOUR MONGO CLIENT TOKEN"

# First create a Github instance using an access token
g = Github(ACCESS_TOKEN)

# Mongo connection
client = pymongo.MongoClient(CONNECTION_TO_MONGO)

collection_repos = client["contacts"]["repos"]

def searchOwnerInDb(mail):
    element = collection_repos.find_one({"owner mail" : mail})
    return element

def queryJson(code, language):
    data = {}
    data['language'] = language
    data['url'] = code.html_url
    data['owner'] = code.owner.login
    data['owner mail'] = code.owner.email
    return data

def searchRepo(querySearch, language):
    repo = g.search_repositories(query=querySearch)
    for code in repo:
        core_rate_limit = g.get_rate_limit().core
        commits =  code.get_commits()
        if(core_rate_limit.limit < 10):
            print(core_rate_limit)
            print('Waiting for rate limit...')
            time.sleep(3600)

        if commits.totalCount > 1 and code.owner.email!= None:
            if(searchOwnerInDb(code.owner.email)==None):
                data = queryJson(code, language)
                collection_repos.insert_one(data)

# Repositories Q#
searchRepo('language:Q#', 'Q#')

# Repositories OpenQASM
searchRepo('language:openqasm', 'OpenQASM')

# Repositories qiskit
searchRepo('in:readme qiskit language:python', 'Qiskit')

# Repositories cirq
searchRepo('in:readme cirq language:python', 'Cirq')

# Repositories Silq
searchRepo('in:readme silq', 'Silq')

# Repositories Pytket
searchRepo('in:readme pytket language:python', 'Pytket')

# Repositories Pennylane
searchRepo('in:readme pennylane language:python', 'Pennylane')

# Repositories Forest SDK
searchRepo('in:readme pyquil language:python', 'Forest SDK')

# Repositories DWave-Ocean
searchRepo('in:readme dwave language:python', 'D-Wave Ocean')

# Repositories Alibaba
searchRepo('in:readme acqdp language:python', 'Alibaba')

# Repositories Braket AWS
searchRepo('in:readme braket language:python', 'Braket AWS')

# Repositories Quantum Computing Language
searchRepo('in:readme qcl language:python', 'QCL')

# Repositories Quantum Machine Learning
searchRepo('in:readme qml language:python', 'QML')

# Repositories Strawberry Fields
searchRepo('in:readme strawberryfields language:python', 'Strawberry Fields')
