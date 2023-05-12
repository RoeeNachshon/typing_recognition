import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.metrics import accuracy_score
import user
import time
import pandas as pd
import train_ai
import math

"""df = pickle.load(open("db.pkl", "rb")) # 1100
pickle.dump(df,open("plan_b_DB.pkl", "wb"))
df['index'] = (df.index // 100) + 1
df = df.set_index(['index', df.groupby('index').cumcount()])
print(df)"""


df = pickle.load(open("db.pkl", "rb"))



X_train, X_test, = train_test_split(df, test_size=0.25, random_state=1)
clf = OneClassSVM(kernel='rbf')
clf.fit(X_train)
pickle.dump(clf, open('ai.pkl', 'wb'))
print("trained!")

