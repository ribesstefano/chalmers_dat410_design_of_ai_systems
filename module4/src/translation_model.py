from collections import defaultdict as ddict
# import matplotlib as mpl
# import pandas as pd

def train(eng, fr, prtable=None, debug=False):
    if prtable is None:
        prtable = ddict(lambda: 1e-6)
    ec_num = ddict(lambda:1e-6)
    ec_den = ddict(lambda:1e-6)
    # E step
    if debug:
        print('E Step')
    for eSent, fSent in zip(eng, fr):
        # split the words and insert NULL word
        e = eSent.strip().split(' ')
        e.insert(0, 'NULL')
        f = fSent.strip().split(' ')
        l = len(e)
        m = len(f)
        # Calculate the expected counts for E step
        for j in range(m):
            # a = np.zeros(l)
            a = [0] * l
            for i in range(l):
                a[i] = prtable[f[j],e[i]]
                if debug:
                    print('Pr. Lookup:', e[i], f[j], prtable[f[j], e[i]], sum(a))
            a = [x / sum(a) for x in a]
            for i in range(l):
                ec_num[f[j], e[i]] += a[i]
                ec_den[e[i]] += a[i]
    # M Step
    if debug:
        print('M Step')
    for fj, ei in prtable.keys():
        # calculate p(fj|ei) table from expected counts
        prtable[fj, ei] = ec_num[fj, ei]/ec_den[ei]
        if debug:
            print(ei, fj, ec_num[fj, ei], prtable[fj, ei])
    return prtable

def readfile(filename):
    '''reads the file'''
    sentList=[]
    with open(filename,'r') as f:
        for aline in f:
            sentList.append(aline.strip())
    return sentList

def get_prob(prtabel, fw, ew):
    '''given two words returns the probability that the foreign word it's the translation of the english word'''
    key = (fw, ew)
    if key in prtabel.keys():
        return prtabel.get(key)
    else:
        return 0.00001

def is_in_keys(prtabel, ew):
    keys = prtabel.keys()
    f_words = []
    for key in keys:
        if ew in key:
            f_words.append(key[0])
    return f_words

def most_probable_words(prtable, ew, f_words, n):
    '''-prtabel: table of probabilities
     - ew: target language
     - f_words: foreign language vocabulary
     -n : top n most probable words'''
    df = pd.DataFrame(columns=f_words)
    prob = []
    for f_word in f_words:
        prob.append(get_prob(prtable, f_word, ew))
    a_series = pd.Series(prob, index=df.columns)
    df = df.append(a_series, ignore_index=True)
    df = df.sort_values(by=0, ascending=False, axis=1)
    return df.iloc[:,0:n]

def get_bigram_prob(prtabel, f_bigram, e_bigram):
    '''returns the probability that a bigram is correctly translated in a foreign bigram.
    Inputs:
    -probability table
    -foreign bigram
    -english bigram'''

    return get_prob(prtabel, f_bigram[0], e_bigram[0])*get_prob(prtabel, f_bigram[1], e_bigram[1])

if __name__ == '__main__':
    trainlist_eng = readfile('test.eng')
    trainlist_fra = readfile('test.fra')
    prtable = ddict(lambda: 1e-6)
    prtable = train(trainlist_eng,trainlist_fra,prtable)

    prob = get_bigram_prob(prtable, ['nature','cours'], ['nature', 'issues'])

    f_words = is_in_keys(prtable, 'nature')

    df = most_probable_words(prtable, 'european', f_words, 3)

    print(df)
