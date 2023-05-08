from sklearn import svm
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
import user
import pickle

def init():
    df = pickle.load(open('db.pkl', 'rb'))
    trainX_allSamples = df.reset_index().drop(columns=['keys'])
    trainY_allSamples = df.index
    train(trainX_allSamples, trainY_allSamples)

def train(X, y):
    # Split the data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    # Create an SVM classifier with a linear kernel
    clf = svm.SVC(kernel='linear')
    print("fitting....")
    # Train the classifier on the training data
    clf.fit(X_train, y_train)

    # Use the classifier to make predictions on the test data
    y_pred = clf.predict(X_test)

    # Compute the accuracy of the classifier
    accuracy = accuracy_score(y_test, y_pred)

    print("Accuracy:", accuracy)
    pickle.dump(clf, open('ai.pkl', 'wb'))
    print("dumped!")


init()
