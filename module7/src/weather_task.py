from task import Task

class WeatherTask(Task):
    """docstring for WeatherTask"""
    def __init__(self):
        super(WeatherTask, self).__init__()

    def get_queries(self):
        return self.queries