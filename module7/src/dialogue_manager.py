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
        # self._close_task(self._ask_user('How can I help you?'))
        bot_message = 'How can I help you?'
        more_tasks = True
        while more_tasks:
            user_request = self._ask_user(bot_message, acknowledge=False)
            more_tasks = self._close_task(user_request)
            bot_message = 'Is there anything else I can do?'
        self.close()

    def close(self):
        # Just to avoid repeating the closing remarks if the user manually
        # closes the chatbot
        if self.activated:
            self._say('Thank you. Bye.')
        self.activated = False

    def _close_task(self, input_sentence=None, task=None):
        # TODO: How do we handle/recognize that a task has been completed?
        if input_sentence is not None:
            self.user_sentences.append(input_sentence)
            task = self.task_identifier.get_task_from_sentence(input_sentence)
            if task is None:
                return False
            else:
                self._acknowledge_user()
        for query in task.get_queries():
            satisfied_query = False
            # Keep asking questions until the query is satisfied.
            while not satisfied_query:
                for sentence in self.user_sentences:
                    satisfied, reply = task.is_query_satisfied(query, sentence)
                    if not satisfied:
                        self.user_sentences.append(self._ask_user(reply, acknowledge=False))
                    else:
                        self._say(reply)
                        satisfied_query = True
                        if sentence != input_sentence:
                            self.user_sentences.remove(sentence)

        # Task solved, get the solution/ackowledgement
        self._say(task.resolve_queries())
        # Reset sentences from the user
        self.user_sentences = []
        return True

    def _say(self, sentence):
        if sentence != '':
            print('[UBOT] ' + sentence)

    def _ask_user(self, request, acknowledge=True):
        self._say(request)
        user_answer = input('[USER] ')
        if acknowledge:
            self._acknowledge_user()
        return user_answer.lower()

    def _acknowledge_user(self):
        reply = "Thank you. I'll take care of that."
        self._say(reply)

def main():
    dm = DialogueManager()
    dm.activate()
    dm.close()

if __name__ == '__main__':
    main()