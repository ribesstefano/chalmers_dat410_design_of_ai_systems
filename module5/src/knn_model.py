import data_cleaner

import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

def define_model(n):
    return KNeighborsClassifier(n)


def train_model(knn, x_train, y_train, scaler=None):
    if scaler is not None:
        x_train = scaler.fit_transform(x_train)
    knn.fit(x_train, y_train)


def get_scores(knn, x_test, scaler=None):
    if scaler is not None:
        x = scaler.transform(x_test)
    else:
        x = x_test
    return knn.predict_proba(x)


def compute_roc_curve(y_test, y_scores):
    return roc_curve(y_test, y_scores)


def compute_auc(y_test, y_scores):
    return roc_auc_score(y_test, y_scores)


def get_max_auc(x_train, y_train, x_test, y_test, verbose=0):
    if verbose:
        fig, ax = plt.subplots()
    df_scores = pd.DataFrame(data=None, columns=['N', 'AUC', 'Scaled'], )
    best_model = None
    best_auc = -1e31
    best_scaler = None
    minmax_scaler = MinMaxScaler()
    for n in np.arange(1, 51):
        for scaler in [None, minmax_scaler]:
            knn = define_model(n)
            train_model(knn, x_train, y_train, scaler)
            y_scores = get_scores(knn, x_test, scaler)
            fpr, tpr, threshold = compute_roc_curve(y_test, y_scores[:, 1])
            auc = compute_auc(y_test, y_scores[:, 1])
            if auc > best_auc:
                best_auc = auc
                best_model = knn
                best_scaler = scaler
            score_dict = {'N': n, 'AUC': auc, 'Scaled': scaler}
            df_scores = df_scores.append(score_dict, ignore_index=True)
            if verbose:
                print(f'N:{n}, AUC:{auc}, Scaled:{scaler}')
                ax.plot(fpr, tpr)
    if verbose:
        plt.show()
    df_scores = df_scores.sort_values(by=['AUC'], ascending=False)
    return df_scores.iloc[0], best_model, best_scaler


def main():
    x_train, y_train, x_test, y_test = data_cleaner.clean_data('wdbc.pkl', 0.7)
    max_auc, model = get_max_auc(x_train, y_train, x_test, y_test)
    print(max_auc)


if __name__ == '__main__':
    main()
