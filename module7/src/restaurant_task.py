from task import Task

class RestaurantTask(Task):
    """docstring for RestaurantTask"""
    def __init__(self):
        super(RestaurantTask, self).__init__()

    def is_query_satisfied(self, query, sentence):
        return False, ''

    def resolve_queries(self):
        """
        Given all the satisfied queries, resolve the task and return a reply to
        the user.
        
        :returns:   A reply to the user
        :rtype:     str
        """
        return ''