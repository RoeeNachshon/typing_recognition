import keyboard
import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder

from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import make_column_transformer
from sklearn.pipeline import make_pipeline


def encode_features(df, ohe_enc):
    cat = get_categories()
    transformer = make_column_transformer((ohe_enc, [x[0] for x in cat]), remainder='passthrough')
    transformed = transformer.fit_transform(df)
    df = pd.DataFrame(transformed, columns=transformer.get_feature_names_out(), index=df.index)
    return df


def get_enc():
    cat = get_categories()
    enc = OneHotEncoder(handle_unknown='ignore', sparse_output=False, categories=[x[1] for x in cat])
    return enc


def get_categories():
    temp = []
    for i in range(1, 83):
        temp.append(str(i))
    return [('Last key-', temp),
            ('Current key-', temp)]


data = pickle.load(open("db.pkl", "rb"))
data = encode_features(data, get_enc())
pickle.dump(data, open("db.pkl","wb"))
