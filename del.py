import pandas as pd
import pickle
from sklearn.svm import OneClassSVM
import user_dataframe
df = pickle.load(open("oded.pkl", "rb"))
print("\n", df)
#df = user_dataframe.record(100)
ai = pickle.load(open("ai.pkl", "rb"))
df = user_dataframe.norm_dataframe(df)
print("\n", df)
ocsvm_scores_test = ai.score_samples(df.values)

print(ocsvm_scores_test.mean())
