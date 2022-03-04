from task_identifier import TaskIdentifier
from task import Task

class DialogManager(object):
    """docstring for DialogManager"""
    def __init__(self):
        super(DialogManager, self).__init__()
        self.user_sentences = []
        self.task_identifier = TaskIdentifier()

    def formulate_answer(self, input_sentence):
        self.user_sentences.append(input_sentence)

        task = self.task_identifier.get_task_from_sentence(input_sentence)
        all_queries_satisfied = False

        while not all_queries_satisfied:
            all_queries_satisfied = True
            for query in task.get_queries():
                for sentence in self.user_sentences:
                    satisfied, request = task.is_query_satisfied(query, sentence)
                    if not satisfied:
                        self.sentences.append(self.ask_question(request))
                    # If at least one query isn't satisfied, restart all over
                    all_queries_satisfied &= satisfied
        return "I'm a bot."

    def ask_question(self, request):
        print('[BOT]  ' + request)
        user_answer = ''
        self.acknowledge_user(user_answer)
        return user_answer

    def acknowledge_user(self, user_answer):
        reply = "Thank you. I'll take care of that."
        print('[BOT]  ' + reply)

def main():
    dm = DialogManager()
    user_sentence = "What's the weather like tomorrow?"
    bot_answer = dm.formulate_answer(user_sentence)
    print('[USER] ' + user_sentence)
    print('[BOT]  ' + bot_answer)


if __name__ == '__main__':
    main()