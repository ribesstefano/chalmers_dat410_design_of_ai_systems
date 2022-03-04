from task import Task

class RestaurantTask(Task):
    """docstring for RestaurantTask"""
    def __init__(self):
        super(RestaurantTask, self).__init__()

    def is_query_satisfied(self, query, sentence):
        return False, ''