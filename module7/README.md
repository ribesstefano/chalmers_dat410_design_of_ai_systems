# Module 7: Dialogue systems and question answering

The purpose of this task is to make you aware of the basic steps and challenges involved in designing a digital assistant.

## Quick-Start Guide

In oder to run our system, one needs to istall _Spacy_ and its dependencies:

```bash
(env) >>> pip install -U spacy
(env) >>> python -m spacy download en_core_web_lg
```

Once Spacy has been installed, please run:

```bash
(env) >>> cd src/
(env) >>> python dialogue_manager.py
```

## Implementation Details

The main system is managed by the `DialogueManager` class, which is responsible for prompting bot's questions and handle user's replies.

The internal Finite State Machine (FSM) of the `DialogueManager` works as follows:
1. Identify the task that the user is aiming to solve: to do so, the class `TaskIdentifier` returns a task object tailored to the user's request.
2. Given a specific task class, loop over its specific queries and check whether they are satisfied or not.
3. If any of the query is _not_ satisfied, the `DialogueManager` asks a clarification question (which was returned from the task's check on the query)
4. Once all queries are satified, the `DialogueManager` "resolves the task" by prompting the solution or ackowledge from the specific task.
5. Finally, ask if there's any other task to solve: if yes, restart from the first step, otherwise close the program.

## Assignment Summary

### Implementation

Implement a simple text-based digital assistant that can help with at least three things, for example:

* provide a weather forecast
* find a restaurant
* find the next tram/bus

However, implement in such a way that the assistant is extensible to a much larger set of tasks.

Note that it is possible to implement this in a trivial way by having the system fully control the flow like in "Enter 1 for account, 2 for insurance, 3 for loans", and continue in the same way with very specific questions. However, a dialogue system aims for a more flexible style, allowing for a more natural conversation. This is a non-trivial task, and while it is clearly not possible to fully solve in the scope of a weekly project, it is quite possible to get an understanding of many of the issues involved.

We suggest that you implement your assistant in the simplest possible way based on keyword matching (at least at first). Also think of the assistant as having access to back-end systems with the appropriate databases and functionality - for the purpose of this task you can simply use ficticious or random data.

As the output of this task, briefly describe how you have implemented the system, and especially any non-trivial functionality. Show some sample outputs, where the dialogue is as advanced as your system allows. Also show or discuss the limitations of your system. Submit your code in a zip-file separately from the module report.

### Future Directions

Suggest how - if more time were available - you could make your dialogue system more advanced.