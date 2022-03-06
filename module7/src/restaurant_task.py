from task import Task


class RestaurantTask(Task):
    """docstring for RestaurantTask"""

    def __init__(self):
        super(RestaurantTask, self).__init__()
        self.queries = {'location': None, 'type': None}
        self.cusine_set = {'italian', 'indian', 'chinese'}
        self.cities_set = {'Gothenburg', 'Malmo', 'Stockholm', 'Linkoping'}
        self.times_set = {'today', 'tomorrow', 'afternoon', 'morning'}

    def are_queries_satisfied(self):
        queries = self.queries.values()

        for value in queries:
            if value is None:
                return False
        return True

    def get_queries(self, sentence):
        for city in self.cities_set:
            if city in sentence:
                self.queries['location'] = city
        for cusine in self.cusine_set:
            if cusine in sentence:
                print('im here')
                self.queries['type'] = cusine

    def resolve_queries(self):
        """
        Given all the satisfied queries, resolve the task and return a reply to
        the user.
        
        :returns:   A reply to the user
        :rtype:     str
        """
        while not self.are_queries_satisfied():
            if self.queries.get('location') is None:
                city = input('Please provide a location ')
                if city not in self.cities_set:
                    print('City not present in database')
                else:
                    self.queries['location'] = city
            if self.queries.get('type') is None:
                cusine = input('Please provide a type of cusine ')
                if cusine not in self.cusine_set:
                    print(f'Cusine inserted not valid please choose between :{self.cusine_set}')
                else:
                    self.queries['type'] = cusine
        return ''
