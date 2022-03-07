from task import Task

import random

class WeatherTask(Task):
    """docstring for WeatherTask"""
    def __init__(self):
        super(WeatherTask, self).__init__()
        self.times_set = {'today', 'tomorrow', 'in 2 days'}
        self.stops_set = {'gothenburg', 'malmo', 'stockholm'}
        self.queries = {'location': None, 'time': None}
        self.solve_query = {
            'location': self._is_location_satisfied,
            'time': self._is_time_satisfied
        }
        self.forcast = ['cloudy', 'sunny', 'rainy', 'snowy']

    def _is_location_satisfied(self, sentence):
        if self.queries['location'] is None:
            for stop in self.stops_set:
                if stop in sentence:
                    self.queries['location'] = stop
                    return True, ''
            return False, "I dind't find the location. Please tell me a location."
        else:
            True, ''

    def _is_time_satisfied(self, sentence):
        if self.queries['time'] is None:
            for time in self.times_set:
                if time in sentence:
                    self.queries['time'] = time
                    return True, ''
            return False, "I dind't understand when. Please tell me a valid time window."
        else:
            True, ''

    def is_query_satisfied(self, query, sentence):
        # TODO: This might look like an overkill, since the two methods are
        # nearly identical in what they do. However, for a more scalable
        # solution, having them separate might be beneficial.
        return self.solve_query[query](sentence)

    def get_queries(self):
        return self.queries.keys()

    def resolve_queries(self):
        """
        Given all the satisfied queries, resolve the task and return a reply to
        the user.
        
        :returns:   A reply to the user
        :rtype:     str
        """
        city = self.queries['location']
        at_time = self.queries['time']
        forcast = random.choice(self.forcast)
        reply = f'{at_time} the weather in {city} is {forcast}'
        return reply
