import re
from collections import Counter
from itertools import islice

def open_file(name):
    with open(name, 'r') as f:
        text = f.read()
    return text

def clean_text(text):
    text = re.sub(r'[^\w ]', '', text)
    return text.split(' ')

def count_words(word_list, verbose=0):
    ''' counter '''
    c = Counter(word_list)
    if verbose:
        print(c.most_common(10))
    return c

def get_word_counter(filename):
    return count_words(clean_text(open_file(filename)))

def get_bigram_counter(filename):
    txt = open_file(filename)
    words = re.findall(r'\w+', txt)
    return Counter(zip(words, islice(words, 1, None)))
    # return Counter(zip(txt, txt[1:]))

if __name__ == '__main__':
    text = open_file("data/dat410_europarl/europarl-v7.de-en.lc.de")
    word_list = clean_text(text)
    c = count_words(word_list)