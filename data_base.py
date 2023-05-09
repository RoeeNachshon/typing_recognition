import pickle

df = pickle.load(open("db.pkl", "rb"))
df = df[:-50]
pickle.dump(df, open("db.pkl","wb"))
