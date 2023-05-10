import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM


def train(data_base):
    """
    Trains the AI according to the params.
    :param data_base: The data to train the AI on
    :return: Dumps the AI in "ai.pkl"
    """
    X_train, X_test, = train_test_split(data_base, test_size=0.25, random_state=1)
    clf = OneClassSVM(kernel='linear', nu=0.245)
    clf.fit(X_train)
    pickle.dump(clf, open('ai.pkl', 'wb'))
    # evaluate the accuracy of the model


def get_accuracy(ns):
    """
    Tests the accuracy of the current AI.
    :param ns: Manager name space
    :return: A number of the AI's accuracy
    """
    X_train, X_test, = train_test_split(ns.ud, test_size=0.5, random_state=1)
    y_predict = ns.ai.predict(X_test)
    acc = accuracy_score([1] * len(X_test), y_predict)
    return acc


def cut_df(ns, wanted_char_count):
    """
    Cuts the existing data frame by the params.
    :param ns: Manager name space
    :param wanted_char_count: The wanted amount of chars to be cut from the data base
    :return: Dumps the new data base in "db.pkl"
    """
    df = pickle.load(open("db.pkl", "rb"))
    df = df[:-wanted_char_count]
    ns.db = df
    pickle.dump(df, open("db.pkl", "wb"))
