from collections import defaultdict as ddict
import numpy as np
import matplotlib as mpl

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
    sentList=[]
    with open(filename,'r') as f:
        for aline in f:
            sentList.append(aline.strip())
    return sentList

trainlist_eng = readfile('test.eng')
trainlist_fra = readfile('test.fra')
prtable = ddict(lambda: 1e-6)
prtable = train(trainlist_eng,trainlist_fra,prtable)

print(prtable)
