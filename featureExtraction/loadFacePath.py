
import pandas as pd

def loadFaceData(path):
	dataFrame = pd.read_csv(path)
	X = dataFrame['path']
	y = dataFrame['class']
	return X, y

if __name__ == '__main__':
	X, y = loadFaceData('face.csv')
	print(X)
	print(y)