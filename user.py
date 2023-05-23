import keyboard
import pandas as pd
import pickle
import sys


def create_timing_lists(wanted_char_count):
    """
    Creates two lists of timings (press and release) and one of keys.
    :param wanted_char_count: The wanted amount of chars to be measured
    :return: Lists of press times, release times, and keys names
    """
    key_press_lst = []
    key_release_lst = []
    key_list = []
    for i in range((wanted_char_count * 2) + 10):
        event = keyboard.read_event()
        if event.event_type == "down" and len(key_press_lst) <= wanted_char_count:
            key_press_lst.append(event.time)
        if event.event_type == "up" and len(key_release_lst) <= wanted_char_count:
            key_release_lst.append(event.time)
            key_list.append(event.scan_code)
    return key_press_lst, key_release_lst, key_list


def calculate_key_durations(press_times, release_times):
    """
    Calculates the times durations keyboard of events into three lists.
    :param press_times: A list of time of the keys press times
    :param release_times: A list of time of the keys release times
    :return: Lists of hold duration, time between two key presses and time between release press
    """
    key_hold_durations = []
    time_between_keys = []
    time_between_release_press = []

    # Check that both lists have the same length
    if not lengths_check(press_times, release_times):
        print("Error: press_times and release_times must have the same length.", len(release_times), len(press_times))
        return [], [], []

    for i in range(len(press_times)):

        key_hold_durations.append(round((release_times[i] - press_times[i]), 3) * 1000)

        if i > 0:
            time_between_keys.append(round((press_times[i] - press_times[i - 1]), 3) * 1000)
        if i < len(press_times) - 1:
            time_between_release_press.append(round((press_times[i + 1] - release_times[i]), 3) * 1000)

    return key_hold_durations, time_between_keys, time_between_release_press


def lengths_check(press_times, release_times):
    return len(press_times) == len(release_times)


def create_table_mat(key_list, hd_list, ppd_list, rpd_list):
    """
    Creates the pandas data frame from the params.
    :param key_list: List of the keys pressed
    :param hd_list: Hold duration of a key
    :param rpd_list: Time between release and next press
    :param ppd_list: Time between two presses
    :return: Pandas data frame
    """
    last_key = [-1]
    last_key.extend(key_list)
    dataframe = pd.DataFrame(list(zip(last_key, key_list, hd_list, rpd_list, ppd_list)),
                             columns=["Last key-", "Current key-", "HD-", "RPD-", "PPD-"])
    return dataframe


def record(wanted_char_count):
    """
    Gets the user typing data by the param.
    :param wanted_char_count: The wanted amount of chars to be measured
    :return: Pandas data frame
    """
    key_press_time, key_release_time, key_list = create_timing_lists(wanted_char_count)
    hold_durations, press_press_durations, release_press_durations = calculate_key_durations(key_press_time,
                                                                                             key_release_time)
    data_frame = create_table_mat(key_list, hold_durations, press_press_durations, release_press_durations)
    return data_frame
