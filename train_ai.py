import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM

def train(data):
    X_train, X_test, = train_test_split(data, test_size=0.25, random_state=1)
    clf = OneClassSVM(kernel='linear', nu=0.245)
    clf.fit(X_train)
    pickle.dump(clf, open('ai.pkl', 'wb'))
    # evaluate the accuracy of the model
