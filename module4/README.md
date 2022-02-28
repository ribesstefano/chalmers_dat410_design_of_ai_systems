# Natural Language Processing

## Instructions

In order to run the assignment, please run the `main` function in file `src/decoder.py`.
The code has been written in Python 3 and should not depend on any library outside the standard libraries.

## Assignment Text

Repeat the lecture slides that describe word-based statistical machine translation. You may also read the following introduction to IBM models 1 and 2 (Links to an external site.), by Michael Collins. You will implement the algorithm described in Figure 4, but please note that the pseudocode is a bit confusing and includes some things you don't need. Here is a document that gives a neater description of the algorithm that estimates the parameters of IBM model 1.

The following file contains a number of sentence-aligned parallel texts taken from the European Parliament proceedings (Links to an external site.). The file contains Swedish-English, German-English, and French-English sentence pairs. For instance, the file europarl-v7.sv-en.lc.sv contains the Swedish part of the Swedish-English dataset. The texts have been preprocessed to be more easy to work with: all words are in lowercase, and punctuation has been separated from the words. This means that you can split each sentence into separate words simply by considering the whitespace.

## (a) Warmup.

As a warmup, write code to collect statistics about word frequencies in the two languages. Print the 10 most frequent words in each language.

If you're working with Python, using a Counter (Links to an external site.) is probably the easiest solution.

Let's assume that we pick a word completely randomly from the European parliament proceedings. According to your estimate, what is the probability that it is speaker? What is the probability that it is zebra?

## (b) Language modeling.

We will now define a language model that lets us compute probabilities for individual English sentences.
Implement a bigram language model as described in the lecture, and use it to compute the probability of a short sentence.

What happens if you try to compute the probability of a sentence that contains a word that did not appear in the training texts? And what happens if your sentence is very long (e.g. 100 words or more)? Optionally, change your code so that it can handle these challenges.

## (c) Translation modeling.

We will now estimate the parameters of the translation model P(f|e).

Self-check: if our goal is to translate from some language into English, why does our conditional probability seem to be written backwards? Why don't we estimate P(e|f) instead?

Write code that implements the estimation algorithm for IBM model 1. Then print, for either Swedish, German, or French, the 10 words that the English word european is most likely to be translated into, according to your estimate. It can be interesting to look at this list of 10 words and see how it changes during the EM iterations.

## (d) Decoding.

Define and implement an algorithm to find a translation, given a sentence in the source language. That is, you should try to find
```
E* = argmaxE P(E|F)
```

In plain words, for a given source-language sentence F, we want to find the English-language sentence E that has the highest probability according to the probabilistic model we have discussed. Using machine translation jargon, we call this algorithm the "decoder." In practice, you can't solve this problem exactly and you'll have to come up with some sort of approximation.

Exemplify how this algorithm works by showing the result of applying your translation system to a short sentence from the source language.

As mentioned, it is expected that you will need to introduce a number of assumptions to make this at all feasible. Please explain all simplifying assumptions that you have made, and the impact you think that they will have on the quality of translations. But why is it an algorithmically difficult problem to find the English sentence that has the highest probability in our model?


## TODOs

* `language_model.py`: What's the count of bigrams when the sentence has an odd number of words?