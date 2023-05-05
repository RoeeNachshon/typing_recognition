import user
import train_ai

df = user.get_user_initial_data()
train_ai.fit(df)
ai = pickle.load(open('ai.pkl', 'rb'))
print(ai)

