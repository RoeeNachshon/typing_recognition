import time
from pynput import keyboard
import pandas as pd
import keyboard
import numpy as np


def create_timing_lists():
    key_press_lst = []
    key_release_lst = []
    key_list = []
    while len(key_press_lst) < 50:
        event = keyboard.read_event()
        if event.event_type == "down":
            key_press_lst.append(event.time)
            key_list.append(event.name + "_p")
        if event.event_type == "up":
            key_release_lst.append(event.time)
            key_list.append(event.name + "_r")
    return key_press_lst, key_release_lst, key_list


def make_lists(key_press_time, key_release_time):
    PPD_list = []
    HD_list = []
    RPD_list = [key_press_time[1]]
    for i in range(len(key_release_time)):
        HD_list.append(round(key_release_time[i] - key_press_time[i], 3) * 1000)
        RPD_list[i] = round(key_press_time[i] - RPD_list[-1], 3) * 1000
        RPD_list.append(key_press_time[i])
        PPD_list.append(float(RPD_list[len(RPD_list) - 2]) + float(HD_list[-1]))
    PPD_list[0] = -1
    RPD_list[0] = -1
    return HD_list, PPD_list, RPD_list[:-1]


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
    return new_list


def arrange_index_df(df, key_list):
    sorted_key_list = sort_key_list(key_list)
    df['keys'] = sorted_key_list
    df = df.reset_index().set_index('keys')
    df = df.drop(columns=['index'])
    return df


def get_user_initial_data(turns):
    new_data_frame = pd.DataFrame()
    while len(new_data_frame) < turns:
        print("Write!")
        key_press_time, key_release_time, key_list = create_timing_lists()
        keyboard.read_event()  # clean the remaining key
        HD_list, PPD_list, RPD_list = make_lists(key_press_time, key_release_time)
        press_list = create_press_timestamps_lst(PPD_list)
        data_frame = create_table_mat(HD_list, PPD_list, RPD_list, press_list)
        data_frame = create_bins(data_frame)
        data_frame = arrange_index_df(data_frame, key_list)
        print("Yap!", "\n", data_frame)
    return new_data_frame


if __name__ == '__main__':
    print(get_user_initial_data(1))
