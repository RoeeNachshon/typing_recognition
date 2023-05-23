import pandas as pd
import pickle
from sklearn.svm import OneClassSVM
import user_dataframe
df = user_dataframe.record(100)
ai = pickle.load(open("ai.pkl","rb"))
print(df)
ocsvm_scores_test = ai.score_samples(df.values)

print(ocsvm_scores_test.mean())