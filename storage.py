"""storage.py"""
from utils import Singleton
from models import Log
from typing import List

class InMemoryStorage(metaclass=Singleton):
    def __init__(self):
        self.messages = []
    
    def save(self, message: Log) -> None:
        self.messages.append(message.dict())

    def list(self) -> List[str]:
        ordered_list = sorted(self.messages, key=lambda x: x["created_at"])
        return [x["message"] for x in ordered_list]