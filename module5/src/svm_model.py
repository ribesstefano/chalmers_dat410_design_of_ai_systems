import data_cleaner

import pandas as pd
from sklearn.svm import SVC
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

svc = SVC()
kernels = {'poly', 'rbf', 'sigmoid'}


def define_model(n, kernel):
    return SVC(C=n, kernel=kernel)


def train_model(svc, x_train, y_train, scaler=None):
    if scaler is not None:
        x_train = scaler.fit_transform(x_train)
    svc.fit(x_train, y_train)


def get_scores(svc, x_test, scaler=None):
    if scaler is not None:
        x = scaler.transform(x_test)
    else:
        x = x_test
    return svc.decision_function(x)


def compute_roc_curve(y_test, y_scores):
    return roc_curve(y_test, y_scores)


def compute_auc(y_test, y_scores):
    return roc_auc_score(y_test, y_scores)


def get_max_auc(x_train, y_train, x_test, y_test, verbose=0):
    if verbose:
        fig, ax = plt.subplots()
    df_scores = pd.DataFrame(data=None, columns=['C', 'Kernel', 'AUC', 'Scaled'], )
    best_model = None
    best_auc = -1e31
    best_scaler = None
    minmax_scaler = MinMaxScaler()
    for c in np.arange(0.1, 5.1, 0.1):
        for kernel in ['poly', 'rbf', 'sigmoid']:
            for scaler in [None, minmax_scaler]:
                svc = define_model(c, kernel)
                train_model(svc, x_train, y_train, scaler)
                y_scores = get_scores(svc, x_test, scaler)
                fpr, tpr, threshold = compute_roc_curve(y_test, y_scores)
                auc = compute_auc(y_test, y_scores)
                if auc > best_auc:
                    best_auc = auc
                    best_model = svc
                    best_scaler = scaler
                score_dict = {'C': c, 'Kernel': kernel, 'AUC': auc, 'Scaled': scaler}
                df_scores = df_scores.append(score_dict, ignore_index=True)
                if verbose:
                    print(f'C:{c}, Kernel:{kernel}, AUC:{auc}, Scaled:{scaler}')
                    ax.plot(fpr, tpr)

    if verbose:
        plt.xlabel('False Positive')
        plt.ylabel('True Positive')
        fig1 = plt.gcf()
        plt.show()
        fig1.savefig('trade_off.png')

    df_scores = df_scores.sort_values(by=['AUC'], ascending=False)
    return df_scores.iloc[0], best_model, best_scaler


def main():
    x_train, y_train, x_test, y_test = data_cleaner.clean_data('wdbc.pkl', 0.7)
    max_auc = get_max_auc(x_train, y_train, x_test, y_test)
    print(max_auc)


if __name__ == '__main__':
    main()
