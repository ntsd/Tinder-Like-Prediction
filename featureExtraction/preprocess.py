import cv2
import numpy as np
from Feature import Feature
from sklearn.preprocessing import normalize
from loadFacePath import loadFaceData
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.linear_model import SGDClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score, accuracy_score
from sklearn.svm import LinearSVC

if __name__ == "__main__":
    f = Feature()
    paths, classes = loadFaceData('face.csv')
    X = []
    y = []
    # add face not found class
    # for i in range(5):
    #     X.append(np.zeros(shape=(128)))
    #     y.append('Face_Not_Found')
    for index, path in enumerate(paths):
        if index == 82:
            break
        ar = f.getFeature(path)
        print(index, path)
        if ar.all() == 0:
            continue
            X.append(ar)
            y.append('Face_Not_Found')
        X.append(ar)
        y.append(classes[index])
    # print(y)
    # print(X)
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
    