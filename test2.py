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
db_for_train = pd.DataFrame()


def learn_user(lst, ns):
    num_of_tests = lst[0]
    need_create_db = lst[1]
    print("starting RECORDING", num_of_tests)
    new_user_data = user.get_user_initial_data(num_of_tests)
    frames = [ns.ud, new_user_data]
    ns.ud = pd.concat(frames)
    if need_create_db:
        create_db(num_of_tests, ns)
    else:
        renew_db(num_of_tests, ns)


def renew_db(num_of_tests, ns):
    data = pickle.load(open('db.pkl', 'rb'))
    id_lst = train_ai.create_id_list((len(data.index)-880)+num_of_tests)
    frames = [data, ns.ud]
    data = pd.concat(frames)
    data['user'] = id_lst
    data = data.reset_index().set_index('user')
    ns.db = data.drop(columns=['index'])
    pickle.dump(ns.db, open('db.pkl', 'wb'))


def create_db(num_of_tests, ns):
    data = data_base.get_DB()
    id_lst = train_ai.create_id_list(num_of_tests)
    frames = [data, ns.ud]
    data = pd.concat(frames)
    data['user'] = id_lst
    data = data.reset_index().set_index('user')
    ns.db = data.drop(columns=['index'])
    pickle.dump(ns.db, open('db.pkl', 'wb'))

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


def init_ai(ns):
    learn_user([8, True],ns)
    # fit_ai()
    #  for the first few runs (the missing sta ing 8 us)


def turn_off():
    # ctypes.windll.user32.LockWorkStation()
    print("Turned OFF!")


def threads(num_of_tests, ns):
    init_ai(ns)
    print("end of innit")
    record_user_data_thread = Process(target=learn_user, args=([num_of_tests, False], ns))
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
    ns = mgr.Namespace()
    ns.ai = pickled_model
    ns.ud = user_data
    ns.db = db_for_train

    threads(1, ns)
