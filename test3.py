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

X_train, X_test, = train_test_split(data, test_size=0.25, random_state=1)

clf = OneClassSVM(kernel='linear', nu=0.245)
clf.fit(X_train)

# Predict the labels of the test set using the trained One-Class SVM
y_pred = clf.predict(X_test)

# Print the predicted labels and the actual labels of the test set
print("Predicted labels:", y_pred)

# evaluate the accuracy of the model
accuracy = accuracy_score([1] * len(X_test), y_pred)
print('Accuracy:', accuracy)

print('*************************************************************************************')

# load the data from a CSV file
testData = pickle.load(open('oded.pkl', 'rb'))
# Predict the labels of the test set using the trained One-Class SVM
z_pred = clf.predict(testData)

# Print the predicted labels and the actual labels of the test set
print("Predicted labels:", z_pred)

# evaluate the accuracy of the model
accuracy = accuracy_score([1] * len(testData), z_pred)
print('Accuracy:', accuracy)
