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


def learn_user(ns, wanted_char_count):
    print("starting LEARNING")
    while 1:
        df = user.get_user_initial_data(wanted_char_count)
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
    print("starting FITTING")
    count = 1
    while 1:
        if len(ns.db) % 1000 == count:
            train_ai.train(ns.db)
            ns.ai = pickle.load(open('ai.pkl', 'rb'))
            count += 1


def test_ai(ns, wanted_char_count):
    print("starting TESTING")
    while 1:
        if ctypes.windll.user32.GetForegroundWindow() != 0:  # while not on lockscreen
            wanted_acc_value = 0.6
            if not ns.ud.empty:
                acc = train_ai.get_accuracy(ns)
                is_above_accuracy_value = acc <= wanted_acc_value
                if not is_above_accuracy_value:
                    turn_off(ns, wanted_char_count)


def turn_off(ns, wanted_char_count):
    ns.ud = pd.DataFrame()
    ctypes.windll.user32.LockWorkStation()
    cut_df(ns, wanted_char_count)
    print("Turned OFF!")


def processes(ns, wanted_char_count):
    fit_ai_process = Process(target=fit_ai, args=(ns,))
    record_user_data_process = Process(target=learn_user, args=(ns, wanted_char_count))
    test_ai_process = Process(target=test_ai, args=(ns, wanted_char_count))
    record_user_data_process.start()
    test_ai_process.start()
    fit_ai_process.start()
    fit_ai_process.join()
    record_user_data_process.join()
    test_ai_process.join()


if __name__ == '__main__':
    char_count = 100
    mgr = Manager()
    name_space = mgr.Namespace()
    name_space.ai = pickled_model
    name_space.ud = user_data
    name_space.db = data_base
    processes(name_space, char_count)
