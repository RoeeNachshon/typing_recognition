import pickle
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM
from sklearn.metrics import accuracy_score
import user
import time

df = user.get_user_initial_data(100)
ai = pickle.load(open("ai.pkl","rb"))
X_train, X_test, = train_test_split(df, test_size=0.25, random_state=1)
y_predict = ai.predict(X_test)
acc = accuracy_score([1] * len(X_test), y_predict)
print(acc)

"""db = pickle.load(open("db.pkl","rb"))

X_train, X_test, = train_test_split(db, test_size=0.25, random_state=1)
clf = OneClassSVM(kernel='linear', nu=0.245)
clf.fit(X_train)
pickle.dump(clf, open('ai.pkl', 'wb'))"""

