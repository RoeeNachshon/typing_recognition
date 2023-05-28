import pandas as pd
import pickle
from sklearn.ensemble import IsolationForest
import user_dataframe
from sklearn.svm import OneClassSVM
from sklearn.metrics import classification_report

"""features = pickle.load(open("oded.pkl", "rb"))
print(features)
isof = IsolationForest(random_state = 0).fit(features.values)
ocsvm_scores_test = isof.predict(features.values)
count = 0
print(ocsvm_scores_test)
for val in ocsvm_scores_test:
    if val == 1:
        count += 1

print((count / 100) * 100, "%")
print(isof.score_samples(features.values).mean())
#pickle.dump(isof,open("isofAI.pkl","wb"))"""


features = pickle.load(open("plan_b_DB_mult.pkl", "rb"))[24900:]
#features = user_dataframe.record(100)
print("\n", features)
ai = pickle.load(open("ai.pkl", "rb"))
isof = pickle.load(open("isofAI.pkl", "rb"))
ocsvm_scores_test = ai.predict(features.values)
isof_scores_test= isof.predict(features.values)
count_ocsvm = 0
count_isof = 0
print(isof_scores_test)
for val in ocsvm_scores_test:
    if val == 1:
        count_ocsvm += 1
for val in isof_scores_test:
    if val == 1:
        count_isof += 1

print((count_ocsvm / 100) * 100, "%")
print((count_isof / 100) * 100, "%")


y_pred = [1 if pred == -1 else 0 for pred in isof_scores_test]

# Step 5: Evaluate model performance
report = classification_report([1]*len(y_pred), y_pred)
print(report)