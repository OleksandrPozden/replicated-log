"""storage.py"""
from utils import Singleton
import logging

class InMemoryStorage(metaclass=Singleton):
    def __init__(self):
        self.messages = []
    
    def save(self, message):
        self.messages.append(message)

    def list(self):
        return self.messages