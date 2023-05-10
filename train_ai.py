import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM


def train(data):
    X_train, X_test, = train_test_split(data, test_size=0.25, random_state=1)
    clf = OneClassSVM(kernel='linear', nu=0.245)
    clf.fit(X_train)
    pickle.dump(clf, open('ai.pkl', 'wb'))
    # evaluate the accuracy of the model


def get_accuracy(ns):
    X_train, X_test, = train_test_split(ns.ud, test_size=0.5, random_state=1)
    y_predict = ns.ai.predict(X_test)
    acc = accuracy_score([1] * len(X_test), y_predict)
    return acc


def cut_df(ns, wanted_char_count):
    df = pickle.load(open("db.pkl", "rb"))
    df = df[:-wanted_char_count]
    ns.db = df
    pickle.dump(df, open("db.pkl", "wb"))
