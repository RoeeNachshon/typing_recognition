import pickle
import pandas as pd
import user
import train_ai
import ctypes
from multiprocessing import Process, Manager
from sklearn.model_selection import train_test_split

pickled_model = pickle.load(open('ai.pkl', 'rb'))  # what happens on first?
data_base = pickle.load(open('db.pkl', 'rb'))
user_data = pd.DataFrame()


def learn_user(ns, wanted_char_count):
    """
    A function built purely to record the user according to the char amount. RUNS CONSTANTLY.
    :param ns: Manager name space
    :param wanted_char_count: The wanted amount of chars to be added to the data base
    :return: Dumps the new data base in "db.pkl"
    """
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
        except FileNotFoundError:
            pickle.dump(df, open('db.pkl', 'wb'))
            fit_ai(ns, wanted_char_count)


def fit_ai(ns, wanted_char_count):
    """
    A function that fits the AI with the newest data base. RUNS CONSTANTLY.
    :param wanted_char_count: Chars until the next fit
    :param ns: Manager name space
    :return: Nothing
    """
    print("starting FITTING")
    db_length = len(ns.db)
    while 1:
        if db_length + 2 * (wanted_char_count - 1) == len(ns.db):
            train_ai.train(ns.db)
            ns.ai = pickle.load(open('ai.pkl', 'rb'))
            db_length = len(ns.db)


def test_ai(ns, wanted_char_count):
    """
    A function to test the AI with the user's data. below a curtain number locks the computer. RUNS CONSTANTLY.
    :param ns: Manager name space
    :param wanted_char_count: The wanted amount of chars to be added to the data base
    :return: Nothing
    """
    print("starting TESTING")
    while 1:
        if ctypes.windll.user32.GetForegroundWindow() != 0:  # while not on lockscreen
            wanted_acc_value = 0.3
            if not ns.ud.empty:
                acc = train_ai.get_accuracy(ns)
                is_above_accuracy_value = acc >= wanted_acc_value
                if not is_above_accuracy_value:
                    print(acc)
                    ctypes.windll.user32.LockWorkStation()
                    ns.ud = pd.DataFrame()
                    train_ai.cut_df(ns, wanted_char_count)


def processes(ns, wanted_char_count):
    """
    The "mother function". In charge of initiating all the processes.
    :param ns: Manager name space
    :param wanted_char_count: The wanted amount of chars to be added to the data base
    :return: Nothing
    """
    fit_ai_process = Process(target=fit_ai, args=(ns, wanted_char_count))
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
