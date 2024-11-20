from fastapi import BackgroundTasks
from storage import InMemoryStorage
from datetime import datetime
from fastapi import FastAPI
from fastapi import status
from utils import Singleton
from models import RESTLog
from models import Log
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
        self.replicas = []# or [Replica(id=1, name="name1", host="localhost", port=50051)]
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
            self.replicas = [] or [Replica(id=1, name="name1", host="localhost", port=50051)]

async def save_message(replica: Replica, log: Log):
    channel = grpc.aio.insecure_channel(f'{replica.host}:{replica.port}')
    stub = logger_pb2_grpc.LoggerStub(channel)
    response = await stub.SaveMessage(logger_pb2.LogMessageRequest(message=log.message, created_at=log.created_at))
    return response

async def write_to_remaining_replicas(replica_tasks):
    try:
        await asyncio.gather(*replica_tasks)
    except RuntimeError:
        # usually arises when no tasks to await. rare case but possible
        pass
    
@app.post("/log/create", status_code=status.HTTP_201_CREATED)
async def create_log(input_log: RESTLog, background_tasks: BackgroundTasks):
    message_inserted_at = datetime.now()
    log = Log(message=input_log.message, created_at=message_inserted_at)
    local_storage.save(log)
    tasks = [asyncio.create_task(save_message(replica, log)) for replica in ReplicaContainer()]
    if input_log.write_concern == 1:
        background_tasks.add_task(asyncio.gather, *tasks)
        return {"result": f"Data succesfully saved with write concern: {input_log.write_concern}"}
    
    completed_tasks = []
    for task in asyncio.as_completed(tasks):
        finished_task = await task
        completed_tasks.append(finished_task)
        if len(completed_tasks) > input_log.write_concern - 1:
            remaining_tasks = [t for t in tasks if not t.done()]
            background_tasks.add_task(asyncio.gather, *remaining_tasks)
            return {"result": f"Data succesfully saved with write concern: {input_log.write_concern}"}
    
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
