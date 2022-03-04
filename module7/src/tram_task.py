from task import Task

class TramTask(Task):
    """docstring for TramTask"""
    def __init__(self):
        super(TramTask, self).__init__()

    def is_query_satisfied(self, query, sentence):
        return False, ''