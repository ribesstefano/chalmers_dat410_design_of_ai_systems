from task import Task
from weather_task import WeatherTask
from restaurant_task import RestaurantTask
from tram_task import TramTask
import spacy

nlp = spacy.load('en_core_web_lg')

weather_string = nlp('What is the weather forcast in the city?')
restaurant_string = nlp('What is the closest Italian restaurant?')
tram_string = nlp('When is the next tram from the station?')


class TaskIdentifier(object):
    """docstring for TaskIdentifier"""

    def __init__(self):
        super(TaskIdentifier, self).__init__()
        self.task_dic = {nlp(' '.join([str(t) for t in weather_string if t.pos_ in ['NOUN', 'PROPN']])): WeatherTask(),
                         nlp(' '.join(
                             [str(t) for t in restaurant_string if t.pos_ in ['NOUN', 'PROPN']])): RestaurantTask(),
                         nlp(' '.join([str(t) for t in tram_string if t.pos_ in ['NOUN', 'PROPN']])): TramTask()
                         }

    def get_task_from_sentence(self, sentence):
        # Analyze sentence and return a specific task class
        nlp_sentence = nlp(sentence)
        no_verbs_sentence = nlp(' '.join([str(t) for t in nlp_sentence if t.pos_ in ['NOUN', 'PROPN']]))
        task_sentences = list(self.task_dic.keys())
        similarity_array = []
        print(task_sentences)

        for ref_sentence in task_sentences:
            similarity_array.append(no_verbs_sentence.similarity(ref_sentence))

        index = similarity_array.index(max(similarity_array))

        # print(self.task_dic[task_sentences[index]])

        return self.task_dic[task_sentences[index]]
