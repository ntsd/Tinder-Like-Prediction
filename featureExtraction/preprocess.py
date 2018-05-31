import cv2
import numpy as np
from Feature import Feature
from sklearn.preprocessing import normalize
from loadFacePath import loadFaceData
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn.model_selection import train_test_split
from sklearn.metrics import f1_score

def norm_size(img_path, points):
    img = cv2.imread(img_path)
    height, width, _ = img.shape
    print(height, width)
    return [ (point.x/width, point.y/height) for point in points]


if __name__ == "__main__":
    f = Feature()
    paths, classes = loadFaceData('face.csv')
    X = []
    y = []
    for index, path in enumerate(paths):
        ar = f.getFeature(path)
        if ar == None:
            continue
        norm_arr = norm_size(path, ar)
        X.append(norm_arr)
        y.append(classes[index])
        if index == 10:
            break
    # print(y)
    # print(X)
    X = np.array(X)
    y = np.array(y)
    print(X.shape)
    print(X)
    print(X.reshape(11, 136))
    X_train_data, X_test_data, y_train_data, y_test_data = train_test_split(X, y, test_size=0.3, stratify=y)
    nearestCentroid = NearestCentroid()
    nearestCentroid.fit(X_train_data, y_train_data)

    predict_y = nearestCentroid.predict(X_test_data)
    f1Score = f1_score(y_test_data, predict_y, average='macro')

    print(f1Score)
    