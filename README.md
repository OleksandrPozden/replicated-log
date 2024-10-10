# Replicated Log | Distributed Systems

## How to run 

`docker-compose up --scale replica=3`

To replicate more or less nodes of the secondaries (replicas) servers replace `3` with any number you want.

## API (master node)

Master node support REST API.
After running docker-compose you will be available to reach the docs on the page:

http://localhost:8000/docs#/

## API (secondaries nodes)

Secondaries nodes support only gRPC interface
