from abc import ABC
from abc import abstractmethod

class Task(ABC):
    """docstring for Task"""
    def __init__(self):
        super(Task, self).__init__()
        # TODO: Using a dictionary instead??
        self.queries = []
        self.satisfied_queries = []

    def get_queries(self):
        return self.queries

    @abstractmethod
    def is_query_satisfied(self, query, sentence):
        # TODO: We need a system to keep track which queries have already been
        # satisfied, such that we don't require to recompute heavy calculations
        pass