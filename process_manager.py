import pickle
import pandas as pd
import user
import train_ai
import ctypes
from multiprocessing import Process, Manager
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

pickled_model = pickle.load(open('ai.pkl', 'rb'))  # what happens on first?
data_base = pickle.load(open('db.pkl', 'rb'))
user_data = pd.DataFrame()


def learn_user(ns):
    print("starting LEARNING")
    while 1:
        df = user.get_user_initial_data()
        ns.ud = df
        try:
            old_data = pickle.load(open('db.pkl', 'rb'))
            frames = [old_data, df]
            ns.db = pd.concat(frames)
            if not ns.ud.empty:
                pickle.dump(ns.db, open('db.pkl', 'wb'))
                print("Renewed!")
        except FileNotFoundError:
            pickle.dump(df, open('db.pkl', 'wb'))
            fit_ai(ns)


def fit_ai(ns):
    # fits the ai with existing db
    print("starting FITTING")
    train_ai.train(ns.db)
    ns.ai = pickle.load(open('ai.pkl', 'rb'))


def test_ai(ns):
    print("starting TESTING")
    process = Process(target=fit_ai, args=(ns,))
    while 1:
        if ctypes.windll.user32.GetForegroundWindow() != 0:  # while not on lockscreen
            accuracy_value = 0.6
            if not ns.ud.empty:
                acc = get_accuracy(ns)
                is_above_accuracy_value = accuracy_check(accuracy_value, acc)
                if not is_above_accuracy_value:
                    turn_off(ns)
                else:
                    process.start()
                    process.join()
            # predict -> acc_check


def get_accuracy(ns):
    X_train, X_test, = train_test_split(ns.ud, test_size=0.5, random_state=1)
    y_predict = ns.ai.predict(X_test)
    acc = accuracy_score([1] * len(X_test), y_predict)
    print(acc)
    return acc


def accuracy_check(wanted_acc_value, acc):
    if acc < wanted_acc_value:
        return False
    return True
    # bellow a number is fail


def turn_off(ns):
    ns.ud = pd.DataFrame()
    ctypes.windll.user32.LockWorkStation()
    print("Turned OFF!")


def threads(ns):
    record_user_data_process = Process(target=learn_user, args=(ns,))
    test_ai_process = Process(target=test_ai, args=(ns,))
    record_user_data_process.start()
    test_ai_process.start()
    record_user_data_process.join()
    test_ai_process.join()
    # thread for - fitting, testing+acc_check, recording user


if __name__ == '__main__':
    mgr = Manager()
    name_space = mgr.Namespace()
    name_space.ai = pickled_model
    name_space.ud = user_data
    name_space.db = data_base
    threads(name_space)
