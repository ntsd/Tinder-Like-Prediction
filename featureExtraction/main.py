
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
	new_dataset=1
	if new_dataset:
		df = pd.read_csv('./dataset/af1and5.csv', nrows=100)
		paths = df['path']
		classes = df['class']
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
	predict_prob = svm.predict_proba(X_test)

	print(predict_prob)

	acc = accuracy_score(y_test, predict_y)

	print(acc)

if __name__ == '__main__':
	scut_fbp_test()
