from task_identifier import TaskIdentifier
from task import Task

class DialogueManager(object):
    """docstring for DialogueManager"""
    def __init__(self, activate=False):
        super(DialogueManager, self).__init__()
        self.user_sentences = []
        self.task_identifier = TaskIdentifier()
        self.activated = False
        if activate:
            self.activate()

    def activate(self):
        print('=' * 80)
        print('*** The UBOT Task Assistant is activated ***')
        print('Ask information about weather, restaurants and trams.')
        print('=' * 80)
        self.activated = True
        new_task = self._interact_with_user(self._ask_user('How can I help you?'))
        while new_task is not None:
            self._acknowledge_user(user_reply)
            new_task = self._interact_with_user(task=new_task)
        self.close()

    def close(self):
        # Just to avoid repeating the closing remarks if the user manually
        # closes the chatbot
        if self.activated:
            self._say('Thank you. Bye.')
        self.activated = False

    def _interact_with_user(self, input_sentence=None, task=None):
        # TODO: How do we handle/recognize that a task has been completed?
        if input_sentence is not None:
            self.user_sentences.append(input_sentence)
            task = self.task_identifier.get_task_from_sentence(input_sentence)

        all_queries_satisfied = False
        while not all_queries_satisfied:
            all_queries_satisfied = True
            for sentence in self.user_sentences:
                for query in task.get_queries(sentence):
                    satisfied, reply = task.is_query_satisfied(query, sentence)
                    if not satisfied:
                        self.user_sentences.append(self._ask_user(reply))
                    else:
                        self._say(reply)
                    # If at least one query isn't satisfied, restart all over
                    all_queries_satisfied &= satisfied
        # Task solved, formulate solution/ackowledge
        self._say(task.resolve_queries())
        self.user_sentences = []
        # TODO: Check what happens when the user gives affermative answers but
        # without any other informative content...
        user_reply = self._ask_user('Is there anything else I can do?', acknowledge=False)
        return self.task_identifier.get_task_from_sentence(user_reply)

    def _say(self, sentence):
        if sentence != '':
            print('[UBOT] ' + sentence)

    def _ask_user(self, request, acknowledge=True):
        self._say(request)
        user_answer = input('[USER] ')
        if acknowledge:
            self._acknowledge_user(user_answer)
        return user_answer

    def _acknowledge_user(self, user_answer=None):
        reply = "Thank you. I'll take care of that."
        self._say(reply)

def main():
    dm = DialogueManager()
    dm.activate()
    dm.close()

if __name__ == '__main__':
    main()