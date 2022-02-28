from data_cleaner import clean_data
import os
import numpy as np
from matplotlib import pyplot as plt

class RuleBasedClassifier(object):
    """Implements a rule-based classifier"""
    def __init__(self):
        super(RuleBasedClassifier, self).__init__()
        self.trained = False
        self.abnormal_cell_size_threshold = 0.
        self.abnormal_cell_shape_threshold = 0.
        self.abnormal_cell_texture_threshold = 0.
        self.abnormal_cell_similarity_threshold = 0.

    def get_mean(self, cell, feature):
        return cell[feature + '_0']

    def get_std(self, cell, feature):
        return cell[feature + '_1']

    def get_worst(self, cell, feature):
        return cell[feature + '_2']

    def fit(self, X, y):
        self.trained = True

        y.describe().transpose()
        pos = X[y == 1]
        neg = X[y == 0]

        # plt.hist(pos['symmetry_mean'] / pos['fractal dimension_mean'], label='pos')
        # plt.hist(neg['symmetry_mean'] / neg['fractal dimension_mean'], label='neg')
        # plt.legend()
        # plt.show()

        self.abnormal_cell_size_threshold = pos['radius_std'].mean()
        self.abnormal_cell_shape_threshold = pos['smoothness_mean'].mean()

        self.abnormal_cell_texture_threshold = pos['concavity_worst'].mean()
        self.abnormal_cell_similarity_threshold = (neg['symmetry_worst'] / neg['fractal dimension_worst']).mean()

    def is_cell_size_abnormal(self, cell):
        if cell['radius_std'] > self.abnormal_cell_size_threshold:
            return True
        else:
            return False

    def is_cell_shape_abnormal(self, cell):
        if cell['smoothness_mean'] > self.abnormal_cell_shape_threshold:
            return True
        else:
            return False

    def is_cell_texture_abnormal(self, cell):
        if cell['concavity_worst'] > self.abnormal_cell_texture_threshold:
            return True
        else:
            return False

    def is_cell_similarity_abnormal(self, cell):
        similarity = cell['symmetry_mean'] / cell['fractal dimension_mean']
        if similarity > self.abnormal_cell_similarity_threshold:
            return True
        else:
            return False

    def predict(self, X):
        if not self.trained:
            print('WARNING. The model has not been trained.')
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
    data_dir = os.path.join(os.path.dirname( __file__ ), '..', 'data')
    data_dir = os.path.abspath(data_dir)
    DATABASE = os.path.join(data_dir, 'wdbc.pkl')
    TRAIN_PERC = 0.8

    data = clean_data(DATABASE, TRAIN_PERC, df_as_numpy=False)
    x_train, y_train, x_test, y_test = data

    model = RuleBasedClassifier()

    model.fit(x_train, y_train)
    print(model.score(x_test, y_test))

if __name__ == '__main__':
    main()
