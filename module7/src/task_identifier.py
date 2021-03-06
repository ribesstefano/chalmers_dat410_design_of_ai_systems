from task import Task
from weather_task import WeatherTask
from restaurant_task import RestaurantTask
from tram_task import TramTask
from nothing_task import NothingTask

import spacy
import warnings

class TaskIdentifier(object):
    """docstring for TaskIdentifier"""
    def __init__(self):
        super(TaskIdentifier, self).__init__()
        self.nlp = spacy.load('en_core_web_lg')
        weather_sample = self.nlp('What is the weather forcast in the city? Thanks')
        restaurant_sample = self.nlp('What is the closest Italian restaurant? Thanks')
        tram_sample = self.nlp('When is the next tram from the station? Thanks')
        quit_sample = self.nlp('I do not need anything thanks')
        self.task_dic = {
            self._remove_verbs(weather_sample) : WeatherTask(),
            self._remove_verbs(restaurant_sample) : RestaurantTask(),
            self._remove_verbs(tram_sample) : TramTask(),
            self._remove_verbs(quit_sample) : None
        }

    def _remove_verbs(self, sentence):
        return self.nlp(' '.join([str(t) for t in sentence if t.pos_ in ['NOUN', 'PROPN']]))

    def get_task_from_sentence(self, sentence):
        # Analyze sentence and return a specific task class
        nlp_sentence = self._remove_verbs(self.nlp(sentence))
        task_sentences = list(self.task_dic.keys())
        similarity_array = []
        with warnings.catch_warnings(): # Suppress warnings from Spacy
            warnings.simplefilter('ignore')
            for ref_sentence in task_sentences:
                similarity_array.append(nlp_sentence.similarity(ref_sentence))
        if max(similarity_array) < 0.75:
            return NothingTask()
        index = similarity_array.index(max(similarity_array))
        return self.task_dic[task_sentences[index]]
