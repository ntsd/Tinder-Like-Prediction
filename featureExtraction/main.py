
import time
import pandas as pd
import numpy as np

# model
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.linear_model import SGDClassifier
from sklearn.svm import LinearSVC, SVC

# prepocess
from preprocess import preprocess
from sklearn.model_selection import train_test_split

# Evaluate metrics
from sklearn.metrics import roc_auc_score, log_loss, accuracy_score

def scut_fbp_test():
    new_dataset=0
    if new_dataset:
        df = pd.read_csv('./dataset/af1and5.csv', nrows=10)
        paths = df['path']
        lasses = df['class']
        X, y = preprocess(paths, classes)
        np.save('X', X)
        np.save('y', y)
    else:
        X=np.load('X.npy')
        y=np.load('y.npy')

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, stratify=y)

    svm = SVC(kernel = 'linear', probability=True)
    svm.fit(X_train, y_train)

    predict_y = svm.predict(X_test)
    
    acc = accuracy_score(y_test, predict_y)
    print(acc)

    predict_prob = svm.predict_proba(X_test)
    print(predict_prob)

    predict_log_loss = log_loss(y_test, predict_prob)
    print(predict_log_loss)

def cross_validation():
    from sklearn.model_selection import KFold
    new_dataset=1
    if new_dataset:
        df = pd.read_csv('./dataset/af1and5.csv')
        paths = df['path']
        classes = df['class']
        X, y = preprocess(paths, classes)
        np.save('X', X)
        np.save('y', y)
    else:
        X=np.load('X.npy')
        y=np.load('y.npy')

    kf = KFold(n_splits=5)
    for train_index, test_index in kf.split(X):
        X_train, X_test = X[train_index], X[test_index]
        y_train, y_test = y[train_index], y[test_index]




if __name__ == '__main__':
    cross_validation()
