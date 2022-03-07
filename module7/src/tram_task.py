from task import Task

class TramTask(Task):
    """docstring for TramTask"""
    def __init__(self):
        super(TramTask, self).__init__()
        self.times_set = {'now', 'in 5 minutes', 'in 1 hour'}
        self.stops_set ={'korsvagen', 'brunnsparken', 'jarntorget'}
        self.queries = {'location': None, 'time': None}
        self.solve_query = {
            'location': self._is_location_satisfied,
            'time': self._is_time_satisfied}

    def is_query_satisfied(self, query, sentence):
        # TODO: This might look like an overkill, since the two methods are
        # nearly identical in what they do. However, for a more scalable
        # solution, having them separate might be beneficial.
        return self.solve_query[query](sentence)

    def _is_location_satisfied(self, sentence):
        if self.queries['location'] is None:
            stop_found = True
            for stop in self.stops_set:
                if stop not in sentence:
                    stop_found = False
                else:
                    self.queries['location'] = stop
                    break
            if stop_found:
                return True, ''
            else:
                return False, 'Location not found. Please provide a location.'
        else:
            True, ''

    def _is_time_satisfied(self, sentence):
        if self.queries['time'] is None:
            time_found = True
            for time in self.times_set:
                if time not in sentence:
                    time_found = False
                else:
                    self.queries['time'] = time
                    break
            if time_found:
                return True, ''
            else:
                return False, 'Invalid time. Please provide a valid time window.'
        else:
            True, ''

    def get_queries(self, sentence):
        return self.queries.keys()

    def resolve_queries(self):
        """
        Given all the satisfied queries, resolve the task and return a reply to
        the user.
        
        :returns:   A reply to the user
        :rtype:     str
        """
        destination = self.queries['location']
        at_time = self.queries[time]
        reply = f'Tram to {destination} will departure {at_time}'
        return reply
