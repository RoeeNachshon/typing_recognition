import pickle
import pandas as pd
import user
import data_base
import train_ai
import ctypes
from multiprocessing import Process, Manager
import numpy as np

pickled_model = pickle.load(open('ai.pkl', 'rb'))
user_data = pd.DataFrame()


def learn_user(ns):
    while 1:
        df = get_user_initial_data()
        ns.ud = df
        try:
            old_data = pickle.load(open('db.pkl', 'rb'))
            frames = [old_data, df]
            df = pd.concat(frames)
            pickle.dump(df, open('db.pkl', 'wb'))
        except FileNotFoundError:
            pickle.dump(df, open('db.pkl', 'wb'))
        ns.db = df


def fit_ai(ns):
    # fits the ai with existing db
    print("starting FITTING")
    train_ai.fit(ns.db)
    ns.ai = pickle.load(open('ai.pkl', 'rb'))


def test_ai(ns):
    print("starting TESTING", ns.ud)
    accuracy_value = 0.7
    predictions = ns.ai.best_estimator_.predict(ns.ud)
    print(predictions, "**********************************")
    is_above_accuracy_value = accuracy_check(predictions, accuracy_value)
    if not is_above_accuracy_value:
        turn_off()
    # predict -> acc_check


def accuracy_check(predictions, wanted_acc_value):
    count_of_correct_predictions = np.count_nonzero(predictions == 110)
    if count_of_correct_predictions / len(predictions) < wanted_acc_value:
        return False
    return True
    # bellow a number is fail


def turn_off():
    # ctypes.windll.user32.LockWorkStation()
    print("Turned OFF!")


def threads(ns):
    record_user_data_thread = Process(target=learn_user, args=(ns,))
    test_ai_thread = Process(target=test_ai, args=(ns,))
    fit_ai_thread = Process(target=fit_ai, args=(ns,))
    record_user_data_thread.start()
    test_ai_thread.start()
    fit_ai_thread.start()
    record_user_data_thread.join()
    test_ai_thread.join()
    fit_ai_thread.join()
    # thread for - fitting, testing+acc_check, recording user


if __name__ == '__main__':
    mgr = Manager()
    name_space = mgr.Namespace()
    name_space.ai = pickled_model
    name_space.ud = user_data
    name_space.db = db_for_train
    threads(name_space)
