import numpy as np

class KNeighborsClassifier(object):
    """
    KNeighborsClassifier implements k-nearest neighbours algorithm. Inspired to
    the scikit learn implementation.
    """
    def __init__(self, n_neighbors=5, weigthts='uniform'):
        super(KNeighborsClassifier, self).__init__()
        self.n_neighbors = n_neighbors
        self.weigthts = weigthts
        self.X = None
        self.y = None
        self.n_features = 0
        self.n_samples = 0
        
    def fit(self, X, y):
        """
        Store the training parameters later used for classification.

        :param      X:               The training data
        :type       X:               Numpy array, shape: (n_samples, n_features)
        :param      y:               The labels of each data point
        :type       y:               Numpy array, shape: (n_samples)

        :raises     AssertionError:  Error when mismatching dimensions
        """
        self.X = np.array(X)
        self.y = np.array(y)
        assert self.X.shape[0] == self.y.shape[0], 'ERROR. Different number of samples for X and y.'

    def predict(self, X):
        """
        Predict the classes of the input array of queries X.

        :param      X:    The queries to classify
        :type       X:    numpy array, shape: (n_queries, n_features)

        :returns:   The numpy array containing the classified labels
        :rtype:     Numpy array, shape: (n_queries)
        """
        labels = np.zeros(X.shape[0])
        for i, x in enumerate(X):
            distances = np.linalg.norm(self.X - x, axis=1)
            neighbors_labels = self.y[np.argsort(distances)[:self.n_neighbors]]
            unique, counts = np.unique(neighbors_labels, return_counts=True)
            labels[i] = unique[np.argmax(counts)]
        return labels

    def score(self, X, y, sample_weight=None):
        pass

def main():
    n_neighbors = 4
    n_samples = 128
    n_features = 8
    n_queries = 32
    knn = KNeighborsClassifier(n_neighbors)
    x_train = np.random.randn(n_samples, n_features)
    y = np.random.randint(n_features, size=n_samples)
    knn.fit(x_train, y)
    print(knn.predict(np.random.randn(n_queries, n_features)))

if __name__ == '__main__':
    main()