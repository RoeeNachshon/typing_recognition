import pandas as pd
import pickle

df = pd.read_pickle(open("db.pkl", "rb"))
pickle.dump(df,open("plan_b_DB.pkl","wb"))