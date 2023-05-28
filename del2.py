import pickle
import pandas as pd
import user_dataframe
from time import time
import csv

filename = r"C:\Users\oded\OneDrive\Desktop\google-python-exercises-master\BioKey-Keystrokes-dynamics-for-continuous-user-authentication\BioKey_Dataset_Collector_ID\roee_data.csv"
text_file = r"C:\Users\oded\OneDrive\Desktop\google-python-exercises-master\typing_recongnition_inc\roee_data_text"

# Open the file in read mode
with open(filename, 'r') as file:
    # Read the contents of the file
    file_contents = file.read()
file_contents = file_contents[8:-4]
lst = file_contents.split("),")
for j in range(len(lst)):
    temp = lst[j].split(",")
    for num in temp:
        if num[1:][0].isdigit():
            with open(text_file, 'a') as file:
                file.write(str(float(num[1:]) / 1000) + " ")
            print(num[1:])
        else:
            if num[2:][-1] != ")":
                with open(text_file, 'a') as file:
                    file.write(str(float(num[2:]) / 1000) + " ")
                print(num[2:])
            else:
                with open(text_file, 'a') as file:
                    file.write(str(float(num[2:-1]) / 1000) + " ")
                print(num[2:-1])

    with open(text_file, 'a') as file:
        file.write("\n")
