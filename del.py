import pandas as pd
import pickle
from sklearn.preprocessing import OneHotEncoder

df = pd.read_pickle(open("db.pkl", "rb"))
print(df)

def min_max_norm(df_, col_name, min_val=-700, max_val=700):
    return (df_[col_name] - min_val) / (max_val - min_val)


def norm_values(df_to_norm):
    for col in ["HD-", "RPD-"]:
        df_to_norm[f"{col}norm"] = min_max_norm(df_to_norm, col)
        df_to_norm[f"{col}norm"] = df_to_norm[f"{col}norm"].apply(lambda x: 1 if x > 1 else x)
        df_to_norm[f"{col}norm"] = df_to_norm[f"{col}norm"].apply(lambda x: 0 if x < 0 else x)
    return df_to_norm

def get_enc():
    enc = OneHotEncoder(handle_unknown='ignore')
    enc.fit(df[['Last key-', "Current key-"]])
    return enc


def encode_features(df_, ohe_enc):
    keys_features_np = ohe_enc.transform(df_[['Last key-', "Current key-"]]).toarray()
    keys_features_df = pd.DataFrame(keys_features_np, columns=ohe_enc.get_feature_names_out())
    return pd.concat([df_[["HD-norm", "RPD-norm"]].reset_index(drop=True), keys_features_df], axis=1)

def norm_dataframe(df):
    enc = get_enc()
    daf = norm_values(df)
    features = encode_features(daf, enc)
    print(features)

df = norm_dataframe(df)
print(df)
#pickle.dump(df,open("db.pkl","wb"))