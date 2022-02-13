from collections import Counter
import re

def open_file(name):
    f = open(name, "r")
    text = f.read()
    return text




# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    deutsch_text = open_file("data/dat410_europarl/europarl-v7.de-en.lc.de")
    deutsch_text = re.sub("[^\w ]", '', deutsch_text)
    deutsch_words = deutsch_text.split(' ')
    deutsch_words = filter(None, deutsch_words)
    c = Counter(deutsch_words)
    print(c.most_common(10))
