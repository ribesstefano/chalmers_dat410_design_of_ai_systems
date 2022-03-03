from task import Task

class RestaurantTask(Task):
    """docstring for RestaurantTask"""
    def __init__(self):
        super(RestaurantTask, self).__init__()

    def get_queries(self):
        return self.queries