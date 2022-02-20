from sklearn.ensemble import RandomForestClassifier
import data_cleaner
from sklearn import metrics
import pandas as pd
import pickle

clf = RandomForestClassifier()

def define_model(n):
    clf = RandomForestClassifier(n_estimators=n)

def train_model(x_train, y_train):

    clf.fit(x_train, y_train)

    return clf

def predict_model(x_test):

    return clf.predict(x_test)

def score_model(y_pred, y_test):
    return metrics.accuracy_score(y_test, y_pred)

def feature_importance(x_train):
    feature_imp = pd.Series(clf.feature_importances_, index=x_train.columns).sort_values(ascending=False)
    return feature_imp

def open_file(filename):
    with open(filename, 'rb') as f:
        df = pickle.load(f)
        return df

def main():
    define_model(10)
    x_train, y_train, x_test, y_test = data_cleaner.clean_data('wdbc.pkl', 0.7, df_as_numpy=False)
    train_model(x_train,y_train)
    y_pred = predict_model(x_test)
    score = score_model(y_pred,y_test)
    importance = feature_importance(x_train)

    print(score,'\n', importance)


if __name__ == '__main__':
    main()