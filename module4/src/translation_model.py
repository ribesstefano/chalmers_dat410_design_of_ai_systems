from collections import defaultdict as ddict
import numpy as np

def train(eng,fr,prtable,debug=False):
    ec_num = ddict(lambda:1e-6)
    ec_den = ddict(lambda:1e-6)
    # E step
    if debug:
        print('E Step')
    for eSent,fSent in zip(eng,fr):
        # split the words and insert NULL word
        e = eSent.strip().split(' ')
        e.insert(0,'NULL')
        f = fSent.strip().split(' ')
        l = len(e)
        m = len(f)
        # Calculate the expected counts for E step
        for j in range(m):
            a = np.zeros(l)
            for i in range(l):
                a[i]=prtable[f[j],e[i]]
                if debug:
                    print('Pr. Lookup:',e[i],f[j],prtable[f[j],e[i]],np.sum(a))
            a = a/np.sum(a)
            for i in range(l):
                ec_num[f[j],e[i]] += a[i]
                ec_den[e[i]]+=a[i]
    # M Step
    if debug:
        print('M Step')
    for fj,ei in prtable.keys():
        # calculate p(fj|ei) table from expected counts
        prtable[fj,ei] = ec_num[fj,ei]/ec_den[ei]
        if debug:
            print(ei,fj,ec_num[fj,ei],prtable[fj,ei])
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



def get_bigram_prob(prtabel, f_bigram, e_bigram):
    '''returns the probability that a bigram is correctly translated in a foreign bigram.
    Inputs:
    -probability table
    -foreign bigram
    -english bigram'''

    return get_prob(prtabel, f_bigram[0], e_bigram[0])*get_prob(prtabel, f_bigram[1], e_bigram[1])

trainlist_eng = readfile('test.eng')
trainlist_fra = readfile('test.fra')
prtable = ddict(lambda: 1e-6)
prtable = train(trainlist_eng,trainlist_fra,prtable)


prob = get_bigram_prob(prtable, ['nature','cours'], ['nature', 'issues'])

print(prob)

# print(prtable)
