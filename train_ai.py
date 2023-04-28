import pandas as pd
import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.metrics import accuracy_score
from sklearn.preprocessing import LabelEncoder
import pickle
from sklearn.model_selection import GridSearchCV, StratifiedShuffleSplit
from xgboost.sklearn import XGBClassifier
import user
import data_base


def create_id_list(num_of_tests):
    id_lst = []
    count = 1
    for i in range(110):
        for j in range(8):
            id_lst.append(count)
        count += 1
    for i in range(num_of_tests):
        id_lst.append(111)
    return id_lst


def fit(trainDF_User_AllSampleProps):
    print(trainDF_User_AllSampleProps, "training...")
    trainX_allSamples = trainDF_User_AllSampleProps.reset_index().drop(columns=['user'])
    trainY_allSamples = trainDF_User_AllSampleProps.index

    xgb1 = XGBClassifier(
        learning_rate=0.1,
        n_estimators=10,
        max_depth=5,
        min_child_weight=3,
        gamma=0,
        subsample=0.8,
        colsample_bytree=0.8,
        objective='multi:softmax',
        num_class=trainY_allSamples.nunique(),
        nthread=4,
        seed=27)
    param_search = {
        'learning_rate': [0.05, 0.1],
        'n_estimators': [100, 200, 210, 230, 250, 270, 290, 310, 330],
        'max_depth': range(4, 10, 1)
    }
    gsearch2b = GridSearchCV(estimator=xgb1, param_grid=param_search, scoring='accuracy', n_jobs=4,
                             cv=StratifiedShuffleSplit(n_splits=3, test_size=0.2, random_state=0), verbose=1)
    le = LabelEncoder()
    y_train = le.fit_transform(trainY_allSamples)

    gsearch2b.fit(trainX_allSamples, y_train)

    print('Best Estimator:\n', gsearch2b.best_estimator_)

    sss = StratifiedShuffleSplit(n_splits=5, test_size=0.2, random_state=0)
    accs = []
    for train_index, test_index in sss.split(trainX_allSamples, y_train):
        gsearch2b.best_estimator_.fit(trainX_allSamples.loc[train_index], y_train[train_index])
        acc = accuracy_score(gsearch2b.best_estimator_.predict(trainX_allSamples.loc[test_index]),
                             y_train[test_index])
        print('Accuracy Score:', acc)
        accs += [acc]
    print('Average Accuracy:', sum(accs) / len(accs))
    pickle.dump(gsearch2b, open('ai.pkl', 'wb'))
    print("YAYYYY!!!!!!")

# plt.show()
