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
    key_list = []
    while len(key_press_lst) < 50:
        event = keyboard.read_event()
        if event.event_type == "down":
            key_press_lst.append(event.time)
            key_list.append(event.name+"_p")
        if event.event_type == "up":
            key_release_lst.append(event.time)
            key_list.append(event.name+"_r")
    return key_press_lst, key_release_lst, key_list


def make_lists(key_press_time, key_release_time):
    PPD_list = []
    HD_list = []
    RPD_list = [key_press_time[1]]
    for i in range(len(key_release_time)):
        HD_list.append(round(key_release_time[i] - key_press_time[i], 3) * 1000)
        RPD_list[i] = round(key_press_time[i] - RPD_list[-1], 3) * 1000
        RPD_list.append(key_press_time[i])
        PPD_list.append(float(RPD_list[len(RPD_list) - 2]) - float(HD_list[-1]))
    PPD_list[0] = -1
    RPD_list[0] = -1
    return HD_list, PPD_list, RPD_list[:-1]

def sort_key_list(key_list):
    new_list = []
    for i in range(len(key_list)):
        if key_list[i][-1] == "r":
            new_list.append(key_list[i].split("_")[0])
    return new_list

ls1, ls2, ls3 = create_timing_lists()
new = sort_key_list(ls3)
print(make_lists(ls1, ls2), new)
