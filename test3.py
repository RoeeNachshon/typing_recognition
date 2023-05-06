import user
import pickle

df = user.get_user_initial_data()
ai = pickle.load(open('ai.pkl', 'rb'))
print(ai.predict(df))


