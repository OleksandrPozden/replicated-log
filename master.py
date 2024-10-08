from storage import InMemoryStorage
from pydantic import BaseModel
from fastapi import FastAPI
from fastapi import status
from utils import Singleton
import logger_pb2_grpc
import logger_pb2
import logging
import grpc
import socket


logging.getLogger().setLevel(logging.INFO)

local_storage = InMemoryStorage()

REPLICA_SERVICE_NAME = "replica"

class Log(BaseModel):
    message: str

app = FastAPI()

class Replica:
    def __init__(self, id, name, host, port):
        self.id = id
        self.name = name
        self.host = host
        self.port = port

class ReplicaContainer(metaclass=Singleton):

    def __init__(self):
        self.replicas = []
        self.refresh()

    def __iter__(self):
        return iter(self.replicas)
    
    def add(self, replica: Replica):
        self.replicas.append(replica)
        self.replicas = list(set(self.replicas))
    
    def list(self):
        return self.replicas
    
    def refresh(self):
        try:
            for host in socket.gethostbyname_ex(REPLICA_SERVICE_NAME)[2]:
                name = socket.gethostbyaddr(host)[0].split('.')[0]
                replica_id = int(name.split('replica-')[-1])
                self.add(Replica(replica_id, name, host, 50051))
        except socket.gaierror:
            self.replicas = []

@app.post("/log/create", status_code=status.HTTP_201_CREATED)
def create_log(log: Log):
    responses = []
    local_storage.save(log.message)
    for replica in ReplicaContainer():
        with grpc.insecure_channel(f'{replica.host}:{replica.port}') as channel:
            stub = logger_pb2_grpc.LoggerStub(channel)
            response = stub.SaveMessage(logger_pb2.LogMessageRequest(message=log.message))
            responses.append(response)
    return {"result": [response.result for response in responses]}
    
@app.get("/log/list")
def list_log():
    return {"result": local_storage.list()}

@app.get("/log/{replica_id}/list")
def list_replica_log(replica_id: int):
    for replica in ReplicaContainer():
        if replica.id == replica_id:
            with grpc.insecure_channel(f'{replica.host}:{replica.port}') as channel:
                stub = logger_pb2_grpc.LoggerStub(channel)
                response = stub.GetAllMessages(logger_pb2.GetListMessageRequest())
                return {"result": list(response.messages)}
    return {"error": "Replica not found"}
    
@app.get("/replica/list")
def list_replicas():
    return {"replicas": list(ReplicaContainer().list())}
    
    
@app.get("/")
def root():
    return {"message": "Runing replicas"}
