import keyboard
import numpy as np
import pickle


def create_timing_lists():
    key_press_lst = []
    key_release_lst = []
    key_list = []
    for i in range(110):
        event = keyboard.read_event()
        if event.event_type == "down" and len(key_press_lst) < 50:
            key_press_lst.append(event.time)
            key_list.append(event.name + "_p")
        if event.event_type == "up" and len(key_release_lst) < 50:
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

    last_release_time = 0
    for i in range(len(press_times)):
        press_time = press_times[i]
        release_time = release_times[i]
        key_hold_duration = round((release_time - press_time), 3) * 1000
        key_hold_durations.append(key_hold_duration)

        if i > 0:
            time_between_keys.append(round((press_time - press_times[i-1]), 3) * 1000)
        if i < len(press_times) - 1:
            time_between_release_press.append(round((press_times[i+1] - release_time) , 3)* 1000)

    return key_hold_durations, time_between_keys, time_between_release_press


while 1:

    key_press_time, key_release_time, key_list = create_timing_lists()
    keyboard.read_event()  # clean the remaining key
    print(calculate_key_durations(key_press_time, key_release_time), key_list)
