import pandas as pd
from sklearn.neighbors import KNeighborsClassifier
import data_cleaner
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import numpy as np
from sklearn.preprocessing import MinMaxScaler

scaler = MinMaxScaler()

knn = KNeighborsClassifier()


def define_model(n):
    global knn
    knn = KNeighborsClassifier(n)


def train_model(x_train, y_train, scaled=True):
    if scaled:
        x_train = scaler.fit_transform(x_train)
    knn.fit(x_train, y_train)


def get_scores(x_test, scaled=True):
    if scaled:
        x_test = scaler.transform(x_test)
    return knn.predict_proba(x_test)


def compute_roc_curve(y_test, y_scores):
    return roc_curve(y_test, y_scores)


def compute_auc(y_test, y_scores):
    return roc_auc_score(y_test, y_scores)


def get_max_auc(x_train, y_train, x_test, y_test):
    df_scores = pd.DataFrame(data=None, columns=['N', 'AUC', 'Scaled'], )
    fig, ax = plt.subplots()
    for n in np.arange(1, 51, 1):
        for scaled in [False, True]:
            define_model(n)
            train_model(x_train, y_train, scaled)
            y_scores = get_scores(x_test, scaled)
            fpr, tpr, threshold = compute_roc_curve(y_test, y_scores[:, 1])
            auc = compute_auc(y_test, y_scores[:, 1])
            print(f'N:{n}, AUC:{auc}, Scaled:{scaled}')
            score_dict = {'N': n, 'AUC': auc, 'Scaled': scaled}
            df_scores = df_scores.append(score_dict, ignore_index=True)
            ax.plot(fpr, tpr)
    plt.show()

    df_scores = df_scores.sort_values(by=['AUC'], ascending=False)
    return df_scores.iloc[0]


def main():
    x_train, y_train, x_test, y_test = data_cleaner.clean_data('wdbc.pkl', 0.7)
    max_auc = get_max_auc(x_train, y_train, x_test, y_test)
    print(max_auc)


if __name__ == '__main__':
    main()
