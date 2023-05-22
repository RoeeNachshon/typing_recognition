import pickle
from sklearn.metrics import accuracy_score
import user

CHAR_COUNT = 100
ACCURACY_THRESHOLD = 0.85


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
    y_predict = model.predict(user_data)
    acc = accuracy_score([1] * len(y_predict), y_predict)
    print(acc)
    return acc


def main():
    print("analyzing ...")
    while True:
        user_data = user.record(CHAR_COUNT)
        is_user = validate(user_data)
        print(is_user)


if __name__ == '__main__':
    main()
