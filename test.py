import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.metrics import accuracy_score
import user
import time
import pandas as pd
import train_ai
import math
import os
df = pickle.load(open("db.pkl", "rb")) # 1100
pickle.dump(df, open("plan_b_DB.pkl", "wb"))
"""df = pickle.load(open("db.pkl", "rb")) # 1100
pickle.dump(df,open("plan_b_DB.pkl", "wb"))
df['index'] = (df.index // 100) + 1
df = df.set_index(['index', df.groupby('index').cumcount()])
print(df)
pickle.dump(df,open("db.pkl", "wb"))

"""
"""df = pickle.load(open("plan_b_DB.pkl", "rb"))
pickle.dump(df,open("db.pkl", "wb"))
#pickle.dump(df, open("db.pkl", "wb"))"""

#df = pd.read_csv(r"C:\Users\oded\OneDrive\Desktop\לימודים\עבודות להגשה\סייבר\out1.csv")
"""df.set_index("index", inplace=True, drop=True)
print(df)
X_train, X_test, = train_test_split(df, test_size=0.25, random_state=1)
print(X_train)
clf = OneClassSVM(kernel='rbf', nu=0.1)
clf.fit(X_train)
pickle.dump(clf, open('ai.pkl', 'wb'))
print("trained!")

y_predict = clf.predict(X_test)
print(y_predict)
acc = accuracy_score([1] * len(X_test), y_predict)
print( acc)"""
