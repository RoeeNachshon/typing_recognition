import pickle

import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.svm import SVC
from sklearn.metrics import accuracy_score
from sklearn.ensemble import BaggingClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
import numpy as np

# load the data from a CSV file
data = pickle.load(open('db.pkl', 'rb'))

X = np.random.rand(100, 10)
y = np.random.randint(0, 2, 100)
Z= data.index
'''
X= data.iloc[:, 0:3]

'''


X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=1, stratify=y)


# Initialize the classifiers
tree_clf = DecisionTreeClassifier()
knn_clf = KNeighborsClassifier()
svm_clf = SVC()

svm_clf.fit(X,y)
knn_clf.fit(X,y)
tree_clf.fit(X,y)
# Create an ensemble of classifiers using bagging
ensemble_clf = BaggingClassifier(base_estimator=[DecisionTreeClassifier(), KNeighborsClassifier(), SVC()])

# Fit the ensemble model on the training data
ensemble_clf.fit(X,y)

print("ss")
