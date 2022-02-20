import pandas as pd
from sklearn.svm import SVC
import data_cleaner
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

svc = SVC()
kernels = {'poly', 'rbf', 'sigmoid'}


def define_model(n, kernel):
    global svc
    svc = SVC(C=n, kernel=kernel)


def train_model(x_train, y_train, scaled=True):
    if (scaled):
        x_train = scaler.fit_transform(x_train)
    svc.fit(x_train, y_train)


def get_scores(x_test, scaled=True):
    if (scaled):
        x_test = scaler.transform(x_test)
    return svc.decision_function(x_test)


def compute_roc_curve(y_test, y_scores):
    return roc_curve(y_test, y_scores)


def compute_auc(y_test, y_scores):
    return roc_auc_score(y_test, y_scores)


def get_max_auc(x_train, y_train, x_test, y_test):
    df_scores = pd.DataFrame(data=None, columns=['C', 'Kernel', 'AUC', 'Scaled'], )
    fig, ax = plt.subplots()
    for c in np.arange(0.01, 5, 0.1):
        for kernel in kernels:
            for scaled in [False, True]:
                define_model(c, kernel)
                train_model(x_train, y_train, scaled)
                y_scores = get_scores(x_test, scaled)
                fpr, tpr, threshold = compute_roc_curve(y_test, y_scores)
                auc = compute_auc(y_test, y_scores)
                print(f'C:{c}, Kernel:{kernel}, AUC:{auc}, Scaled:{scaled}')
                dict = {'C': c, 'Kernel': kernel, 'AUC': auc, 'Scaled': scaled}
                df_scores = df_scores.append(dict, ignore_index=True)

                ax.plot(fpr, tpr)
    plt.show()

    df_scores=df_scores.sort_values(by=['AUC'], ascending=False)
    print(df_scores.iloc[0])


def main():
    x_train, y_train, x_test, y_test = data_cleaner.clean_data('wdbc.pkl', 0.7)
    get_max_auc(x_train, y_train, x_test, y_test)


if __name__ == '__main__':
    main()
