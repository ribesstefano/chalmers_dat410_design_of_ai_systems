from task import Task

class RestaurantTask(Task):
    """docstring for RestaurantTask"""

    def __init__(self):
        super(RestaurantTask, self).__init__()
        self.queries = {'location': None, 'cusine': None, 'time': None}
        self.cuisine_set = {'italian', 'indian', 'chinese'}
        self.cities_set = {'gothenburg', 'malmo', 'stockholm', 'linkoping'}
        self.times_set = {'lunch', 'dinner'}
        self.solve_query = {
            'location': self._is_location_satisfied,
            'time': self._is_time_satisfied,
            'cuisine': self.is_cuisine_satisfied
        }

    def _is_location_satisfied(self, sentence):
        if self.queries['location'] is None:
            for city in self.cities_set:
                if city in sentence:
                    self.queries['location'] = city
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

    def is_cuisine_satisfied(self, sentence):
        if self.queries['cuisine'] is None:
            for cuisine in self.cuisine_set:
                if cuisine in sentence:
                    self.queries['cuisine'] = cuisine
                    return True, ''
            return False, 'I cannot find this cuisine. Please tell me a cuisine that I know.'
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
        cuisine = self.queries['cuisine']
        reply = f'Reservation made at {cuisine} restaurant for {at_time} in {city}'
        return reply
