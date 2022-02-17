from data_cleaner import clean_data

import numpy as np

class RuleBasedClassifier(object):
    """Implements a rule-based classifier"""
    def __init__(self):
        super(RuleBasedClassifier, self).__init__()
        self.trained = False
        self.abnormal_cell_size_threshold = 0.
        self.abnormal_cell_shape_threshold = 0.
        self.abnormal_cell_texture_threshold = 0.
        self.abnormal_cell_similarity_threshold = 0.


    def is_cell_size_abnormal(self, cell):
        return False

    def is_cell_shape_abnormal(self, cell):
        return False

    def is_cell_texture_abnormal(self, cell):
        return False

    def is_cell_similarity_abnormal(self, cell):
        return False

    def fit(self, X, y):
        self.trained = True

        y.describe().transpose()
        pos = X[y == 1]
        neg = X[y == 0]

        print(pos['radius_0'].describe().transpose())
        print(neg['radius_0'].describe().transpose())

        '''
        If [cell size is abnormal]
        or [cell shape is abnormal]
        or [cell texture is abnormal]
        or [cell similarity/homogeneity is abnormal]
        '''

    def predict(self, X):
        if not self.trained:
            print('WARNING. The model has not been trained.')
        '''
        We reject all submissions for which the cell count deviates by more than
        20% from the mean cell count across workers.
        '''
        labels = np.zeros(X.shape[0])
        for i, (index, row) in enumerate(X.iterrows()):
            if self.is_cell_size_abnormal(row) or \
                    self.is_cell_shape_abnormal(row) or \
                    self.is_cell_texture_abnormal(row) or \
                    self.is_cell_similarity_abnormal(row):
                labels[i] = 1
            else:
                labels[i] = 0
        return labels

    def score(self, X, y):
        return np.count_nonzero(y == self.predict(X)) / y.size

def main():
    DATABASE = 'wdbc.pkl'
    TRAIN_PERC = 0.8

    data = clean_data(DATABASE, TRAIN_PERC, df_as_numpy=False)
    x_train, y_train, x_test, y_test = data

    model = RuleBasedClassifier()

    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))

if __name__ == '__main__':
    main()