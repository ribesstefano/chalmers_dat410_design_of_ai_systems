from task import Task


class RestaurantTask(Task):
    """docstring for RestaurantTask"""

    def __init__(self):
        super(RestaurantTask, self).__init__()
        self.queries = {'location': None, 'cusine': None, 'time': None}
        self.cuisine_set = {'italian', 'indian', 'chinese'}
        self.cities_set = {'Gothenburg', 'Malmo', 'Stockholm', 'Linkoping'}
        self.times_set = {'lunch', 'dinner'}
        self.solve_query = {
            'location': self._is_location_satisfied,
            'time': self._is_time_satisfied,
            'cuisine': self.is_cuisine_satisfied}

    def _is_location_satisfied(self, sentence):
        if self.queries['location'] is None:
            city_found = True
            for city in self.cities_set:
                if city not in sentence:
                    city_found = False
                else:
                    self.queries['location'] = city
                    break
            if city_found:
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

    def is_cuisine_satisfied(self, sentence):
        if self.queries['cuisine'] is None:
            cuisine_found = True
            for cuisine in self.cuisine_set:
                if cuisine not in sentence:
                    cuisine_found = False
                else:
                    self.queries['cuisine'] = cuisine
                    break
            if cuisine_found:
                return True, ''
            else:
                return False, 'Invalid cuisine. Please provide a valid cuisine type.'
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
