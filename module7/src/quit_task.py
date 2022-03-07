from task import Task

class QuitTask(Task):
    """docstring for WeatherTask"""
    def __init__(self):
        super(QuitTask, self).__init__()
        self.queries = {'quit': None}

    def is_query_satisfied(self, query, sentence):
        return True, ''

    def get_queries(self):
        return self.queries.keys()