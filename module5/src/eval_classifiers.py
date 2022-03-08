import data_cleaner
import knn_model
import svm_model
from random_forest_model import get_feature_importance
from rule_based_model import RuleBasedClassifier

from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import roc_curve, roc_auc_score
import matplotlib.pyplot as plt
import os

def run_rule_based_model(dataset):
    print('INFO. Starting Rule-based evaluation.')
    x_train, y_train, x_test, y_test = dataset
    rulebased = RuleBasedClassifier()
    rulebased.fit(x_train, y_train)
    y_scores = rulebased.predict(x_test)
    auc = roc_auc_score(y_test, y_scores)
    fpr, tpr, threshold = roc_curve(y_test, y_scores)
    return auc, fpr, tpr

def run_random_forest_model(dataset):
    print('INFO. Starting Random Forest evaluation.')
    x_train, y_train, x_test, y_test = dataset
    NUM_ESTIMATORS = 100
    clf = RandomForestClassifier(n_estimators=NUM_ESTIMATORS)
    clf.fit(x_train, y_train)
    y_scores = clf.predict_proba(x_test)
    auc = roc_auc_score(y_test, y_scores[:, 1])
    fpr, tpr, threshold = roc_curve(y_test, y_scores[:, 1])
    print('-' * 80)
    print(f'INFO. Feature ranking:\n{get_feature_importance(clf, x_train)}')
    print('-' * 80)
    return auc, fpr, tpr

def run_knn_model(dataset):
    print('INFO. Starting KNN evaluation.')
    x_train, y_train, x_test, y_test = dataset
    df, knn, knn_scaler = knn_model.get_max_auc(*dataset)
    y_scores = knn_model.get_scores(knn, x_test, knn_scaler)
    auc = roc_auc_score(y_test, y_scores[:, 1])
    fpr, tpr, threshold = roc_curve(y_test, y_scores[:, 1])
    return auc, fpr, tpr

def run_svm_model(dataset):
    print('INFO. Starting SVM evaluation.')
    x_train, y_train, x_test, y_test = dataset
    svm_auc, svm, svm_scaler = svm_model.get_max_auc(*dataset)
    y_scores = svm_model.get_scores(svm, x_test, svm_scaler)
    auc = roc_auc_score(y_test, y_scores)
    fpr, tpr, threshold = roc_curve(y_test, y_scores)
    return auc, fpr, tpr

def main():
    # NOTE: Area Under the Receiver Operating Characteristic Curve (ROC AUC)
    # Clean and split the available data
    TRAIN_PERC = 0.7
    data_dir = os.path.join(os.path.dirname( __file__ ), '..', 'data')
    data_dir = os.path.abspath(data_dir)
    datafile = os.path.join(data_dir, 'wdbc.pkl')
    dataset = data_cleaner.clean_data(datafile, TRAIN_PERC, df_as_numpy=False)
    # Rule-based Classifier
    auc, fpr, tpr = run_rule_based_model(dataset)
    plt.plot(fpr, tpr, label=f'AUC={auc:0.2f} Rule-Based')
    # Random Forest Classifier
    auc, fpr, tpr = run_random_forest_model(dataset)
    plt.plot(fpr, tpr, label=f'AUC={auc:0.2f} Random Forest')
    # KNN Classifier
    auc, fpr, tpr = run_knn_model(dataset)
    plt.plot(fpr, tpr, label=f'AUC={auc:0.2f} KNN')
    # SVC Classifier
    auc, fpr, tpr = run_svm_model(dataset)
    plt.plot(fpr, tpr, label=f'AUC={auc:0.2f} SVM')
    # Final plotting
    plt.plot([0, 1], [0, 1],'--') # Random classifier diagonal line
    plt.title('Receiver Operating Characteristic')
    plt.legend(loc='lower right')
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.grid()
    plt.show()


if __name__ == '__main__':
    main()