from collections import Counter
import re

def open_file(name):
    with open(name, 'r') as f:
        text = f.read()
    return text

def clean_text(text):
    text = re.sub("[^\w ]", '',text)
    return text.split(' ')

def count_words(word_list, verbose=0):
    ''' counter '''
    c = Counter(word_list)
    if verbose:
        print(c.most_common(10))
    return c

def get_counter(filename):
    return count_words(clean_text(open_file(filename)))

if __name__ == '__main__':
    text = open_file("data/dat410_europarl/europarl-v7.de-en.lc.de")
    word_list = clean_text(text)
    c = count_words(word_list)

