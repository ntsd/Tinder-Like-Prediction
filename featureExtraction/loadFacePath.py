
import pandas as pd

def loadFaceData(path, **args):
    dataFrame = pd.read_csv(path, **args)
    X = dataFrame['path']
    y = dataFrame['class']
    return X, y

if __name__ == '__main__':
    X, y = loadFaceData('face.csv')
    print(X)
    print(y)