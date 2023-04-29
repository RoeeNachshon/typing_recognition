import time
from pynput import keyboard
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import keyboard
import numpy as np


def create_timing_lists():
    key_press_lst = []
    key_release_lst = []
    while len(key_press_lst) < 13:
        event = keyboard.read_event()
        if event.event_type == "down":
            key_press_lst.append(event.time)
        if event.event_type == "up":
            key_release_lst.append(event.time)
    while len(key_release_lst) < 13:
        key_release_lst.append(time.time())
    return key_press_lst, key_release_lst


def make_lists(key_press_time, key_release_time):
    PPD_list = [key_press_time[1]]
    HD_list = []
    RPD_list = []
    for i in range(len(key_release_time)):
        HD_list.append(round(key_release_time[i] - key_press_time[i], 3) * 1000)
        PPD_list[i] = round(key_press_time[i] - PPD_list[-1], 3) * 1000
        PPD_list.append(key_press_time[i])
        RPD_list.append(float(PPD_list[len(PPD_list) - 2]) + float(HD_list[-1]))
    PPD_list[0] = -1
    RPD_list[0] = -1
    return HD_list, PPD_list[:-1], RPD_list


def create_histograms(df):
    plt.figure(figsize=(15, 10))
    sns.scatterplot(x='press-', y='PPD-', hue='user', data=df, palette='deep')

    plt.figure(figsize=(15, 10))
    sns.lineplot(x='press-', y='PPD-', hue='user', estimator=None, data=df.reset_index(),
                 palette='deep').set_title('Line plots for each key sequence')


def create_bucket_graph(df):
    plt.figure(figsize=(15, 10))
    plt.subplot(2, 2, 1)
    sns.distplot(df['HD-']).set_title('Hist of Hold Duration')
    plt.subplot(2, 2, 2)
    sns.distplot(df['PPD-']).set_title('Hist of Press-Press Duration')
    plt.subplot(2, 2, 3)
    sns.distplot(df['RPD-']).set_title('Hist of Release-Press Duration')


def create_press_timestamps_lst(PPD_list):
    press_timestamps_lst = [0]  # PPD_lst[0] = -1
    for i in range(1, len(PPD_list)):
        press_timestamps_lst.append(str(round(float(PPD_list[i]) + float(press_timestamps_lst[i - 1]), 3)))
    return press_timestamps_lst


def create_table_mat(HD_list, PPD_list, RPD_list, press):
    key_number = []
    users = []
    for i in range(len(press)):
        key_number.append(i)
        users.append(1)
    df = pd.DataFrame(list(zip(key_number, users, press, HD_list, RPD_list, PPD_list)),
                      columns=["key_no", "user", "press-", "HD-", "RPD-", "PPD-"])
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


def create_column_str(length):
    columns = []
    for i in range(length):
        columns.append("HD_" + str(i))
    for i in range(length):
        columns.append("PPD_" + str(i))
    for i in range(length):
        columns.append("RPD_" + str(i))
    return columns


def get_user_initial_data(turns):
    new_data_frame = pd.DataFrame()
    while len(new_data_frame) < turns:
        print("Write!")
        key_press_time, key_release_time = create_timing_lists()
        keyboard.read_event()  # clean the remaining key
        HD_list, PPD_list, RPD_list = make_lists(key_press_time, key_release_time)
        press_list = create_press_timestamps_lst(PPD_list)
        data_frame = create_table_mat(HD_list, PPD_list, RPD_list, press_list)
        data_frame = create_bins(data_frame)
        res = columns_to_row(data_frame)
        df_to_connect = [new_data_frame, res]
        new_data_frame = pd.concat(df_to_connect)
        print("Yap!")
    return new_data_frame


if __name__ == '__main__':
    print(get_user_initial_data(3))
