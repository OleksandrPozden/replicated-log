"""storage.py"""
from utils import Singleton
from models import Log
from typing import List

class InMemoryStorage(metaclass=Singleton):
    def __init__(self):
        self.__list_hashes = []
        self.messages = []
    
    def save(self, message: Log) -> None:
        if message.hash_id not in self.__list_hashes:
            self.messages.append(message)
            self.__list_hashes.append(message.hash_id)

    def list(self) -> List[str]:
        ordered_list = sorted(self.messages, key=lambda x: x.created_at)
        return [x.message for x in ordered_list]
    
    def _list_raw(self) -> List[Log]:
        return self.messages