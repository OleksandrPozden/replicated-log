from storage import InMemoryStorage
from concurrent import futures
import logger_pb2_grpc
import logger_pb2
import logging
import grpc

logging.getLogger().setLevel(logging.DEBUG)


class LoggerServicer(logger_pb2_grpc.LoggerServicer):
    def SaveMessage(self, request, context):
        logging.info("SaveMessage called")
        InMemoryStorage().save(request.message)
        logging.info(f"Current state is: {InMemoryStorage().list()}")
        return logger_pb2.LogMessageReply(result="201 OK: Sucessfully saved!")
    
    def GetAllMessages(self, request, context):
        logging.info("GetAllMessages called")
        messages = InMemoryStorage().list()
        logging.info(f"Current state is: {messages}")
        return logger_pb2.ListLogMessagesReply(messages=messages)

def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    logger_pb2_grpc.add_LoggerServicer_to_server(LoggerServicer(), server)
    server.add_insecure_port('[::]:50051')
    server.start()
    server.wait_for_termination()

if __name__ == '__main__':
    serve()