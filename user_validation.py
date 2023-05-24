import pickle
from sklearn.metrics import accuracy_score
import user_dataframe

CHAR_COUNT = 100
ACCURACY_THRESHOLD = 4


def load_pickle_file(path: str) -> object:
    return pickle.load(open(path, "rb"))


def validate(user_data) -> bool:
    """
    A function to test the AI with the user's data. below a curtain number locks the computer. RUNS CONSTANTLY.
    :return: Nothing
    """
    return get_accuracy(user_data) >= ACCURACY_THRESHOLD


def get_accuracy(user_data) -> float:
    """
    Tests the accuracy of the current AI.
    :return: A number of the AI's accuracy
    """
    model = load_pickle_file("ai.pkl")
    return model.score_samples(user_data.values)


def main():
    print("analyzing ...")
    while True:
        user_data = user.record(CHAR_COUNT)
        print("\n")
        is_user = validate(user_data)
        print(is_user)


if __name__ == '__main__':
    main()
