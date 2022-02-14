from collections import defaultdict as ddict

def train(eng, fr, prtable=None, verbose=0):
    if prtable is None:
        prtable = ddict(lambda: 1e-6)
    ec_num = ddict(lambda:1e-6)
    ec_den = ddict(lambda:1e-6)
    # E step
    if verbose > 0:
        print('E Step')
    for eSent, fSent in zip(eng, fr):
        # Split the words and insert NULL word
        e = eSent.strip().split(' ')
        e.insert(0, 'NULL')
        f = fSent.strip().split(' ')
        l = len(e)
        m = len(f)
        # Calculate the expected counts for E step
        for j in range(m):
            a = [0] * l
            for i in range(l):
                a[i] = prtable[f[j],e[i]]
                if verbose > 0:
                    print('Pr. Lookup:', e[i], f[j], prtable[f[j], e[i]], sum(a))
            a = [x / sum(a) for x in a]
            for i in range(l):
                ec_num[f[j], e[i]] += a[i]
                ec_den[e[i]] += a[i]
    # M Step
    if verbose > 0:
        print('M Step')
    for fj, ei in prtable.keys():
        # Calculate p(fj|ei) table from expected counts
        prtable[fj, ei] = ec_num[fj, ei] / ec_den[ei]
        if verbose > 0:
            print(ei, fj, ec_num[fj, ei], prtable[fj, ei])
    return prtable

def get_prob(prtable, fw, ew):
    '''
    Given two words returns the probability that the foreign word it's the
    translation of the english word
    
    :param      prtable:  The probability table
    :type       prtable:  Python dictionary with tuple keys: (source word,
                          target word)
    :param      fw:       The target word
    :type       fw:       str
    :param      ew:       The source word
    :type       ew:       str
    
    :returns:   The probability P(fw|ew)
    :rtype:     double
    '''
    key = (fw, ew)
    if key in prtable.keys():
        return prtable.get(key)
    else:
        return 1e-31

def is_in_keys(prtable, ew):
    keys = prtable.keys()
    f_words = []
    for key in keys:
        if ew in key:
            f_words.append(key[0])
    return f_words

def get_best_words(prob_table, src_word):
    """
    Gets the list of best words and probabilities given the source word.
    
    :param      prob_table:  The prob table
    :type       prob_table:  Python dictionary with tuple keys: (source word,
                             target word)
    :param      src_word:    The source word
    :type       src_word:    str
    
    :returns:   The best words.
    :rtype:     list
    """
    probs = [(k, v) for k, v in prob_table.items() if k[0] == src_word]
    return sorted(probs, key=lambda item: item[1], reverse=True)

def get_bigram_prob(prtable, f_bigram, e_bigram, use_log=True):
    '''
    Returns the probability that a bigram is correctly translated in a foreign
    bigram.
    
    :param      prtable:   The prtable
    :type       prtable:   Python dictionary with tuple keys: (source word,
                           target word)
    :param      f_bigram:  The target bigram
    :type       f_bigram:  tuple of strings
    :param      e_bigram:  The source bigram
    :type       e_bigram:  tuple of strings
    :param      use_log:   Whether to use log(P)
    :type       use_log:   bool
    
    :returns:   The bigram probability
    :rtype:     double
    '''
    p_curr = get_prob(prtable, f_bigram[0], e_bigram[0])
    p_next = get_prob(prtable, f_bigram[1], e_bigram[1])
    if use_log:
        return p_curr + p_next
    else:
        return p_curr * p_next

if __name__ == '__main__':
    def readfile(filename):
        sentList=[]
        with open(filename,'r') as f:
            for aline in f:
                sentList.append(aline.strip())
        return sentList

    trainlist_eng = readfile('test.eng')
    trainlist_fra = readfile('test.fra')
    prtable = ddict(lambda: 1e-6)
    prtable = train(trainlist_eng,trainlist_fra,prtable)

    prob = get_bigram_prob(prtable, ['nature','cours'], ['nature', 'issues'])

    f_words = is_in_keys(prtable, 'nature')

    df = most_probable_words(prtable, 'european', f_words, 3)

    print(df)
