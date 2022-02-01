import numpy as np

class KNeighborsClassifier(object):
    """docstring for KNeighborsClassifier"""
    def __init__(self, n_neighbors=5, weigthts='uniform'):
        super(KNeighborsClassifier, self).__init__()
        self.n_neighbors = n_neighbors
        self.weigthts = weigthts
        
    def fit(self, X, y):
        pass

    def predict(self, X):
        pass

    def score(self, X, y, sample_weight=None):
        pass

def main():
    pass

if __name__ == '__main__':
    main()