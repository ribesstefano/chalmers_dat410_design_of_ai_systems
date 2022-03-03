from task import Task

class TramTask(Task):
    """docstring for TramTask"""
    def __init__(self):
        super(TramTask, self).__init__()

    def get_queries(self):
        return self.queries