import numpy as np
from sklearn.svm import OneClassSVM
import pickle
import user


# Load genuine keystroke data
genuine_data = pickle.load(open('db.pkl', 'rb'))

# Train the one-class SVM model
model = pickle.load(open('ai.pkl', 'rb'))

# Test the model on new data
new_data = user.get_user_initial_data()
predictions = model.predict(new_data)

# Print the predictions (genuine=1, outlier=-1)
print(predictions)

