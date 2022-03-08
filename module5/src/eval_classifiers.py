import data_cleaner
import knn_model
import svm_model
from random_forest_model import get_feature_importance
from rule_based_model import RuleBasedClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import os

def main():
    # NOTE: Area Under the Receiver Operating Characteristic Curve (ROC AUC)
    # Clean and split the available data
    TRAIN_PERC = 0.7
    data_dir = os.path.join(os.path.dirname( __file__ ), '..', 'data')
    data_dir = os.path.abspath(data_dir)
    datafile = os.path.join(data_dir, 'wdbc.pkl')
    dataset = data_cleaner.clean_data(datafile, TRAIN_PERC, df_as_numpy=False)
    x_train, y_train, x_test, y_test = dataset
    # Random Forest
    print('INFO. Starting Random Forest evaluation.')
    NUM_ESTIMATORS = 100
    clf = RandomForestClassifier(n_estimators=NUM_ESTIMATORS)
    clf.fit(x_train, y_train)
    y_scores = clf.predict_proba(x_test)
    auc = roc_auc_score(y_test, y_scores[:, 1])
    print(f'INFO. Random Forest ROC AUC: {auc:.4f}')
    # KNN
    print('INFO. Starting KNN evaluation.')
    knn_auc, knn, knn_scaler = knn_model.get_max_auc(*dataset)
    y_scores = knn_model.get_scores(knn, x_test, knn_scaler)
    auc = roc_auc_score(y_test, y_scores[:, 1])
    print(f'INFO. KNN ROC AUC: {auc:.4f}')
    # SVC
    print('INFO. Starting SVC evaluation.')
    svm_auc, svm, svm_scaler = svm_model.get_max_auc(*dataset)
    y_scores = svm_model.get_scores(svm, x_test, svm_scaler)
    auc = roc_auc_score(y_test, y_scores)
    print(f'INFO. SVC ROC AUC: {auc:.4f}')
    # Rule-based
    print('INFO. Starting Rule-based evaluation.')
    rulebased = RuleBasedClassifier()
    rulebased.fit(x_train, y_train)
    y_scores = rulebased.predict(x_test)
    auc = roc_auc_score(y_test, y_scores)
    print(f'INFO. Rule-based ROC AUC: {auc:.4f}')


if __name__ == '__main__':
    main()