from collections import Counter
import re

def open_file(name):
    f = open(name, "r")
    text = f.read()
    return text

def clean_text(text):
    text = re.sub("[^\w ]", '',text)
    return text.split(' ')

def count_words(word_list):
    c = Counter(word_list)
    print(c.most_common(10))
    return c





# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    text = open_file("data/dat410_europarl/europarl-v7.de-en.lc.de")
    word_list = clean_text(text)
    c = count_words(word_list)

