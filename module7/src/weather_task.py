from task import Task


class WeatherTask(Task):
    """docstring for WeatherTask"""

    def __init__(self):
        super(WeatherTask, self).__init__()
        self.queries = {'time': None,
                        'location': None}
        self.cities_set = {'Gothenburg', 'Malmo', 'Stockholm', 'Linkoping'}
        self.times_set = {'today', 'tomorrow', 'afternoon', 'morning'}

    def are_queries_satisfied(self):
        queries = self.queries.values()

        for value in queries:
            if value is None:
                print(value)
                return False

        return True

    def get_queries(self, sentence):
        for time in self.times_set:
            if time in sentence:
                self.queries['time'] = time

        for city in self.cities_set:
            if city in sentence:
                self.queries['location'] = city

    def resolve_queries(self):
        """
        Given all the satisfied queries, resolve the task and return a reply to
        the user.
        
        :returns:   A reply to the user
        :rtype:     str
        """

        while not self.are_queries_satisfied():
            if self.queries.get('location') is None:
                city = input('Please provide a location')
                if city not in self.cities_set:
                    print('City not present in database')
                else:
                    self.queries['location'] = city
            if self.queries.get('time') is None:
                time = input('Please provide a time')
                if time not in self.times_set:
                    print(f'Time inserted not valid please choose between :{self.times_set}')
                else:
                    self.queries['time'] = time

        return ''
