import pickle
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.svm import OneClassSVM


def store_model(model, path: str):
    pickle.dump(model, open(path, "wb"))


def load_training_data(path: str) -> object:
    return pd.read_pickle(open(path, "rb"))


def train(data_base: object) -> object:
    """
    Trains the AI according to the params.
    :param data_base: The data to train the AI on
    :return: Dumps the AI in "ai.pkl"
    """
    model = OneClassSVM(gamma='auto').fit(data_base.values)

    return model


def main():
    data = load_training_data("plan3_db.pkl")

    model = train(data)

    store_model(model, "ai.pkl")


if __name__ == '__main__':
    main()
