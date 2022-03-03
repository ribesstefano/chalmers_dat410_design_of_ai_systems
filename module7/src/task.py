from abc import ABC
from abc import abstractmethod

class Task(ABC):
    """docstring for Task"""
    def __init__(self):
        super(Task, self).__init__()
        self.queries = []

    @abstractmethod
    def get_queries(self):
        return self.queries