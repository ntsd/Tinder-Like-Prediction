import cv2
import time
import numpy as np
import pandas as pd
from Feature import Feature
from sklearn.preprocessing import normalize
from loadFacePath import loadFaceData
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score, mean_absolute_error
from sklearn.svm import LinearSVC, SVC


def preprocess(paths, classes):
    f = Feature()
    X = []
    y = []
    start = time.clock()
    for index, path in enumerate(paths):
        print('Preprocessing', index, path)
        ar = f.getFeature(path)
        if ar.all() == 0:
            continue
        X.append(ar)
        y.append(classes[index])

    test_time = time.clock()-start
    print("Preprocessing Total time: {0:.2f}".format(test_time))
    X = np.array(X)
    y = np.array(y)
    return X, y

def scut_fbp_test():
    f = Feature()
    # af1and5 0.890287769784
    paths, classes = loadFaceData('./dataset/af1and5.csv', nrows=100) # './dataset/all(round_score).csv' for full class
    X = []
    y = []
    for index, path in enumerate(paths):
        ar = f.getFeature(path)
        print(index, path)
        if ar.all() == 0:
            continue
        X.append(ar)
        y.append(round(classes[index]))
    X = np.array(X)
    y = np.array(y)
    print(X.shape)
    print(X)
    print(y)
    X_train_data, X_test_data, y_train_data, y_test_data = train_test_split(X, y, test_size=0.3, stratify=y)
    nearestCentroid = NearestCentroid()
    nearestCentroid.fit(X_train_data, y_train_data)

    predict_y = nearestCentroid.predict(X_test_data)
    acc = accuracy_score(y_test_data, predict_y)

    print(acc)


def flw_dataset_classify():
    f = Feature()
    paths, classes = loadFaceData('face.csv', nrows=82)
    X = []
    y = []
    for index, path in enumerate(paths):
        ar = f.getFeature(path)
        print(index, path)
        if ar.all() == 0:
            continue
        X.append(ar)
        y.append(classes[index])
    X = np.array(X)
    y = np.array(y)
    print(X.shape)
    print(X)
    print(y)
    X_train_data, X_test_data, y_train_data, y_test_data = train_test_split(X, y, test_size=0.3, stratify=y)
    nearestCentroid = NearestCentroid()
    nearestCentroid.fit(X_train_data, y_train_data)

    predict_y = nearestCentroid.predict(X_test_data)
    acc = accuracy_score(y_test_data, predict_y)

    print(acc)

    # Feature Importance
    # from sklearn.ensemble import RandomForestClassifier
    # rf = RandomForestClassifier(random_state=42).fit(X, y)
    # print(rf.feature_importances_)

if __name__ == "__main__": 
    # flw_dataset_classify()
    scut_fbp_test() # result = 0.64
    # preprocess_csv()