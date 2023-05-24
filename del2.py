import pickle
import pandas as pd

data_frame1 = pickle.load(open("db.pkl", "rb"))
print(data_frame1)

