from task import Task

class NothingTask(Task):
    """docstring for WeatherTask"""

    def __init__(self):
        super(NothingTask, self).__init__()
        self.queries = {'nothing': None}

    def is_query_satisfied(self, query, sentence):
        return True, ''

    def get_queries(self):
        return self.queries.keys()

    def resolve_queries(self):
        return 'I\'m not sure I understand your question...'