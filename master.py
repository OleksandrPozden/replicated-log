from storage import InMemoryStorage
from fastapi import FastAPI
from fastapi import status
from utils import Singleton
from models import RESTLog
from models import Log
from time import sleep
import logger_pb2_grpc
import logger_pb2
import logging
import asyncio
import grpc

import socket


logging.getLogger().setLevel(logging.INFO)

REPLICA_SERVICE_NAME = "replica"

local_storage = InMemoryStorage()
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
    
    def count(self):
        return len(self.replicas)
    
    def refresh(self):
        try:
            for host in socket.gethostbyname_ex(REPLICA_SERVICE_NAME)[2]:
                name = socket.gethostbyaddr(host)[0].split('.')[0]
                replica_id = int(name.split('replica-')[-1])
                self.add(Replica(replica_id, name, host, 50051))
        except socket.gaierror:
            self.replicas = []

async def save_message(replica: Replica, message: str):
    channel = grpc.aio.insecure_channel(f'{replica.host}:{replica.port}')
    stub = logger_pb2_grpc.LoggerStub(channel)
    response = await stub.SaveMessage(logger_pb2.LogMessageRequest(message=message))
    return response
    
@app.post("/log/create", status_code=status.HTTP_201_CREATED)
async def create_log(log: RESTLog):
    local_storage.save(log.message)
    tasks = [asyncio.create_task(save_message(replica, log.message)) for replica in ReplicaContainer()] 
    completed_tasks, _ = await asyncio.wait(tasks, return_when=asyncio.ALL_COMPLETED)
    return {"result": [task.result().result for task in list(completed_tasks)]}
    
@app.get("/log/list")
def list_log():
    return {"result": local_storage.list()}

@app.get("/log/{replica_id}/list")
def list_replica_log(replica_id: int):
    for replica in ReplicaContainer():
        if replica.id == replica_id:
            channel = grpc.insecure_channel(f'{replica.host}:{replica.port}')
            stub = logger_pb2_grpc.LoggerStub(channel)
            response = stub.GetAllMessages(logger_pb2.GetListMessageRequest())
            return {"result": list(response.messages)}
    return {"error": "Replica not found"}
    
@app.get("/replica/list")
def list_replicas():
    return {"replicas": list(ReplicaContainer().list())}
    
    
@app.get("/")
def root():
    return {"message": f"Runing {ReplicaContainer().count()} replicas"}
