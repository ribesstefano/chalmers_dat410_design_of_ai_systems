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
        """
        Determines if a query is satisfied in the given sentence.
        
        :param      query:     The query
        :type       query:     { type_description }
        :param      sentence:  The sentence
        :type       sentence:  str
        
        :returns:   True + if query satisfied, False otherwise.
        :rtype:     bool, str
        """
        # TODO: We need a system to keep track which queries have already been
        # satisfied, such that we don't require to recompute heavy calculations
        # (maybe the DialogueManager can take care of that afterall...)
        return False, ''

    @abstractmethod
    def resolve_queries(self):
        """
        Given all the satisfied queries, resolve the task and return a reply to
        the user.
        
        :returns:   A reply to the user
        :rtype:     str
        """
        return ''