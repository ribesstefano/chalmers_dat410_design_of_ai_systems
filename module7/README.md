# Module 7: Dialogue systems and question answering

The purpose of this task is to make you aware of the basic steps and challenges involved in designing a digital assistant.

1. Implement a simple text-based digital assistant that can help with at least three things, for example:

* provide a weather forecast
* find a restaurant
* find the next tram/bus

However, implement in such a way that the assistant is extensible to a much larger set of tasks.

Note that it is possible to implement this in a trivial way by having the system fully control the flow like in "Enter 1 for account, 2 for insurance, 3 for loans", and continue in the same way with very specific questions. However, a dialogue system aims for a more flexible style, allowing for a more natural conversation. This is a non-trivial task, and while it is clearly not possible to fully solve in the scope of a weekly project, it is quite possible to get an understanding of many of the issues involved.

We suggest that you implement your assistant in the simplest possible way based on keyword matching (at least at first). Also think of the assistant as having access to back-end systems with the appropriate databases and functionality - for the purpose of this task you can simply use ficticious or random data.

As the output of this task, briefly describe how you have implemented the system, and especially any non-trivial functionality. Show some sample outputs, where the dialogue is as advanced as your system allows. Also show or discuss the limitations of your system. Submit your code in a zip-file separately from the module report.

2. Suggest how - if more time were available - you could make your dialogue system more advanced.

## Notes

```
1. Natural-language understanding (NLU): prende la frase e genera una query
2. dialog manager (DM): cerca il database e passa l'informazione al NLG
3. Natural language generation (NLG): in base alla request, genera una risposta

1. which task to do: what's the phrase similarity? which information is in the input sentence?
2. Check which information is required to do the task, if anything is missing ask the user to provide it
3. 

class GUI:
	- manages the user interaction

class DM:
	- get_task_from_sentence (i.e. phrase similarity)

	sentences = []
	for query in task.queries:
		satisfied, request = task.is_query_satisfied(query, sentences)
		if not satisfied:
			sentences.append(gui.ask_question(request))

class task:
	- NLU agent/method
	- with a list of queries
```