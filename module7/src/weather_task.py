from task import Task

class WeatherTask(Task):
    """docstring for WeatherTask"""
    def __init__(self):
        super(WeatherTask, self).__init__()
        self.queries = ['time', 'location']

    def is_query_satisfied(self, query, sentence):
        return True, ''

    def resolve_queries(self):
        """
        Given all the satisfied queries, resolve the task and return a reply to
        the user.
        
        :returns:   A reply to the user
        :rtype:     str
        """
        return ''