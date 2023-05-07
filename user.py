import time
from pynput import keyboard
import pandas as pd
import keyboard
import numpy as np
import pickle


def create_timing_lists():
    key_press_lst = []
    key_release_lst = []
    key_list = []
    for i in range(2100):
        event = keyboard.read_event()
        if event.event_type == "down" and len(key_press_lst) < 1000:
            key_press_lst.append(event.time)
            key_list.append(event.name + "_p")
        if event.event_type == "up" and len(key_release_lst) < 1000:
            key_release_lst.append(event.time)
            key_list.append(event.name + "_r")
    return key_press_lst, key_release_lst, key_list


def calculate_key_durations(press_times, release_times):
    key_hold_durations = []
    time_between_keys = []
    time_between_release_press = []

    # Check that both lists have the same length
    if len(press_times) != len(release_times):
        print("Error: press_times and release_times must have the same length.", len(release_times), len(press_times))
        return [], [], []

    for i in range(len(press_times)):
        press_time = press_times[i]
        release_time = release_times[i]
        key_hold_duration = round((release_time - press_time), 3) * 1000
        key_hold_durations.append(key_hold_duration)

        if i > 0:
            time_between_keys.append(round((press_time - press_times[i - 1]), 3) * 1000)
        if i < len(press_times) - 1:
            time_between_release_press.append(round((press_times[i + 1] - release_time), 3) * 1000)

    return key_hold_durations, time_between_keys, time_between_release_press


def create_press_timestamps_lst(PPD_list):
    press_timestamps_lst = [0]  # PPD_lst[0] = -1
    for i in range(1, len(PPD_list)):
        press_timestamps_lst.append(str(round(float(PPD_list[i]) + float(press_timestamps_lst[i - 1]), 3)))
    return press_timestamps_lst


def create_table_mat(HD_list, PPD_list, RPD_list, press):
    df = pd.DataFrame(list(zip(press, HD_list, RPD_list, PPD_list)),
                      columns=["press-", "HD-", "RPD-", "PPD-"])
    return df


def create_bins(df):
    noise = np.random.normal(0, 1e-10, size=len(df))
    df['HD-'] += noise
    df['PPD-'] += noise
    df['RPD-'] += noise
    # to prevent duplicate drops
    noOfBins = 10
    labels = [i for i in range(noOfBins)]
    df['HDEnc'], HDBins = pd.qcut(df['HD-'], retbins=True, labels=labels, q=noOfBins, duplicates='drop')
    df['PPDEnc'], RPDBins = pd.qcut(df['PPD-'], retbins=True, labels=labels, q=noOfBins, duplicates='drop')
    df['RPDEnc'], PPDBins = pd.qcut(df['RPD-'], retbins=True, labels=labels, q=noOfBins, duplicates='drop')

    df['HDEnc'] = df['HDEnc'].astype(str).replace('nan', -1).astype(int)
    df['PPDEnc'] = df['PPDEnc'].astype(str).replace('nan', -1).astype(float)
    df['RPDEnc'] = df['RPDEnc'].astype(str).replace('nan', -1).astype(float)
    return df


def columns_to_row(df):
    HDEnc_lst = df.HDEnc.values.tolist()
    PPDEnc_lst = df.PPDEnc.values.tolist()
    RPDEnc_lst = df.RPDEnc.values.tolist()
    all_list = HDEnc_lst + PPDEnc_lst + RPDEnc_lst
    new_df = pd.DataFrame([all_list])

    columns = create_column_str(len(HDEnc_lst))
    new_df.columns = columns
    return new_df


def sort_key_list(key_list):
    new_list = []
    for i in range(len(key_list)):
        if key_list[i][-1] == "r":
            new_list.append(key_list[i].split("_")[0])
    return new_list[:-1]


def arrange_index_df(df, key_list):
    print(key_list)
    sorted_key_list = sort_key_list(key_list)
    print(sorted_key_list)
    df['keys'] = sorted_key_list
    df = df.reset_index().set_index('keys')
    df = df.drop(columns=['index'])
    df = df.drop(columns=['press-'])
    return df


def get_user_initial_data():
    print("Write!")
    key_press_time, key_release_time, key_list = create_timing_lists()
    keyboard.read_event()  # clean the remaining key
    HD_list, PPD_list, RPD_list = calculate_key_durations(key_press_time, key_release_time)
    press_list = create_press_timestamps_lst(PPD_list)
    data_frame = create_table_mat(HD_list, PPD_list, RPD_list, press_list)
    # data_frame = create_bins(data_frame)
    data_frame = arrange_index_df(data_frame, key_list)
    return data_frame


if __name__ == '__main__':
    data = get_user_initial_data()
    pickle.dump(data, open('db.pkl', 'wb'))
    '''
        while 1:
        df = get_user_initial_data()
            try:
                old_data = pickle.load(open('db.pkl', 'rb'))
                frames = [old_data, df]
                df = pd.concat(frames)
                pickle.dump(df, open('db.pkl', 'wb'))
            except FileNotFoundError:
                pickle.dump(df, open('db.pkl', 'wb'))


    '''
