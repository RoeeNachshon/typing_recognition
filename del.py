import pandas as pd
import pickle
from sklearn.svm import OneClassSVM
import user_dataframe
df = pickle.load(open("plan3_db.pkl", "rb"))
#df = user_dataframe.record(100)
print("\n", df)
ai = pickle.load(open("ai.pkl", "rb"))
ocsvm_scores_test = ai.predict(df.values)
count = 0
for val in ocsvm_scores_test:
    if val ==1:
        count +=1

print(count/2500)  # 1318.9900402133333 //-0.0007407407407407407
