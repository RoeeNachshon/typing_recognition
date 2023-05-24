import keyboard
import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer


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
        elif event.event_type == "up" and len(key_release_lst) <= wanted_char_count:
            key_release_lst.append(event.time)
            key_list.append(event.scan_code)
    return key_press_lst, key_release_lst, key_list


def calculate_key_durations(press_times, release_times):
    """
    Calculates the times durations keyboard of events into three lists.
    :param press_times: A list of time of the keys press times
    :param release_times: A list of time of the keys release times
    :return: Lists of hold duration, time between two key presses, and time between release press
    """
    if len(release_times) == len(press_times):
        key_hold_durations = get_keys_hold_times(press_times, release_times)
        time_between_release_press = get_keys_release_press_times(press_times, release_times)
        return key_hold_durations, time_between_release_press

    print("Error: press_times and release_times must have the same length.", len(release_times), len(press_times))
    return [], []


def get_keys_release_press_times(press_times, release_times):
    return [round((press_times[i + 1] - release_times[i]), 3) * 1000 for i in range(len(press_times) - 1)]


def get_keys_hold_times(press_times, release_times):
    return [round((release_times[i] - press_times[i]), 3) * 1000 for i in range(len(press_times))]


def create_pandas_dataframe(key_list, hd_list, rpd_list):
    """
    Creates the pandas data frame from the params.
    :param key_list: List of the keys pressed
    :param hd_list: Hold duration of a key
    :param rpd_list: Time between release and next press
    :return: Pandas data frame
    """
    last_key = [None]
    last_key.extend(key_list)
    dataframe = pd.DataFrame(list(zip(last_key, key_list, hd_list, rpd_list)),
                             columns=["Last key-", "Current key-", "HD-", "RPD-"])
    return dataframe


def min_max_norm(df_, col_name, min_val=-700, max_val=700):
    return (df_[col_name] - min_val) / (max_val - min_val)


def norm_values(df_to_norm):
    for col in ["HD-", "RPD-"]:
        df_to_norm[f"{col}norm"] = min_max_norm(df_to_norm, col)
        df_to_norm[f"{col}norm"] = df_to_norm[f"{col}norm"].apply(lambda x: 1 if x > 1 else x)
        df_to_norm[f"{col}norm"] = df_to_norm[f"{col}norm"].apply(lambda x: 0 if x < 0 else x)
    return df_to_norm


def get_enc(df):
    cat = get_categories()
    enc = OneHotEncoder(handle_unknown='ignore', sparse_output=False, categories=[x[1] for x in cat])
    return enc


def get_categories():
    temp = []
    for i in range(1, 83):
        temp.append(str(i))
    return [('Last key-', temp),
            ('Current key-', temp)]


def encode_features(df, ohe_enc):
    cat = get_categories()
    transformer = make_column_transformer((ohe_enc, [x[0] for x in cat]), remainder='passthrough')
    transformed = transformer.fit_transform(df)
    df = pd.DataFrame(transformed, columns=transformer.get_feature_names_out(), index=df.index)
    return df


def norm_dataframe(df):
    enc = get_enc(df)
    df = norm_values(df)
    df = encode_features(df, enc)
    df = remove_columns(df)
    return df


def remove_columns(df):
    return df.drop(["remainder__HD-", "remainder__RPD-"], axis=1)


def record(wanted_char_count):
    """
    Gets the user typing data by the param.
    :param wanted_char_count: The wanted amount of chars to be measured
    :return: Pandas data frame
    """
    print("record")
    key_press_times, key_release_times, keys_list = create_timing_lists(wanted_char_count)
    hold_durations, release_press_durations = calculate_key_durations(key_press_times, key_release_times)
    data_frame = create_pandas_dataframe(keys_list, hold_durations, release_press_durations)
    data_frame = norm_dataframe(data_frame)
    return data_frame
