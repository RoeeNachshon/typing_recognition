import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.metrics import accuracy_score
import user
import time
import pandas as pd
import train_ai

df = pickle.load(open("db.pkl", "rb"))
y = pd.DataFrame()
y["before"] = df["Last key-"]
y["current"] = df["Current key-"]

print(y)


X_train, X_test, = train_test_split(df, test_size=0.25, random_state=1)
clf = OneClassSVM(kernel='rbf')
clf.fit(X_train,y)
pickle.dump(clf, open('ai.pkl', 'wb'))
print("trained!")