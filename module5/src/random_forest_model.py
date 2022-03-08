import data_cleaner

from sklearn.ensemble import RandomForestClassifier
from sklearn import metrics
import pandas as pd
import pickle

def define_model(n):
    return RandomForestClassifier(n_estimators=n)

def train_model(clf, x_train, y_train):
    clf.fit(x_train, y_train)
    return clf

def predict_model(clf, x_test):
    return clf.predict(x_test)

def score_model(clf, y_pred, y_test):
    return metrics.accuracy_score(y_test, y_pred)

def get_feature_importance(clf, x_train):
    feature_imp = pd.Series(clf.feature_importances_, index=x_train.columns).sort_values(ascending=False)
    return feature_imp

def main():
    clf = define_model(100)
    x_train, y_train, x_test, y_test = data_cleaner.clean_data('wdbc.pkl', 0.7, df_as_numpy=False)
    train_model(clf, x_train, y_train)
    y_pred = predict_model(clf, x_test)
    score = score_model(clf, y_pred, y_test)
    importance = get_feature_importance(clf, x_train)
    print(score,'\n', importance)


if __name__ == '__main__':
    main()