from task import Task

class TramTask(Task):
    """docstring for TramTask"""
    def __init__(self):
        super(TramTask, self).__init__()
        self.times_set = {'now', '5 minutes', '1 hour'}
        self.queries = {'location': None, 'time': None}
        self.stops_set ={'korsvagen', 'brunnsparken', 'jarntorget'}

    def are_queries_satisfied(self):
        queries = self.queries.values()

        for value in queries:
            if value is None:
                return False
        return True

    def get_queries(self, sentence):
        for stop in self.stops_set:
            if stop in sentence:
                self.queries['location'] = stop
        for time in self.times_set:
            if time in sentence:
                self.queries['time'] = time

    def resolve_queries(self):
        """
        Given all the satisfied queries, resolve the task and return a reply to
        the user.
        
        :returns:   A reply to the user
        :rtype:     str
        """
        while not self.are_queries_satisfied():
            if self.queries.get('location') is None:
                stop = input('Please provide a location ')
                if stop not in self.stops_set:
                    print('City not present in database')
                else:
                    self.queries['location'] = stop
            if self.queries.get('time') is None:
                time = input('Please provide a time ')
                if time not in self.times_set:
                    print(f'Time not valid:{self.times_set}')
                else:
                    self.queries['time'] = time
        return ''
