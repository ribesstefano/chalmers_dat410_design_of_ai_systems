from task import Task
from weather_task import WeatherTask
from restaurant_task import RestaurantTask
from tram_task import TramTask

class TaskIdentifier(object):
    """docstring for TaskIdentifier"""
    def __init__(self):
        super(TaskIdentifier, self).__init__()

    def get_task_from_sentence(self, sentence):
        # Analyze sentence and return a specific task class
        task = WeatherTask()
        return task