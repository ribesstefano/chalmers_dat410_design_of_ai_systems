from task import Task

class WeatherTask(Task):
    """docstring for WeatherTask"""
    def __init__(self):
        super(WeatherTask, self).__init__()
        self.queries = ['time', 'location']

    def is_query_satisfied(self, query, sentence):
        return True, ''