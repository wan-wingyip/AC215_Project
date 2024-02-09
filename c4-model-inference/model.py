import pickle
from sklearn.linear_model import LinearRegression
from sklearn.datasets import load_boston
import pandas as pd

class FinalModel:
    def __init__(self, model = None):
        self.model = model

    def train_model(self, X_train, y_train):
        if self.model is None:
            self.model = LinearRegression()
        self.model.fit(X_train, y_train)
        print("Model has been trained")

    def save_model(self, filename):
        if self.model is None:
            raise ValueError("No model currently exists!")
        with open(filename, 'wb') as file:
            pickle.dump(self.model, file)
        print("Model saved as ", filename)


boston_dataset = load_boston()
boston = pd.DataFrame(boston_dataset.data, columns=boston_dataset.feature_names)
boston["MEDV"] = boston_dataset.target

X = boston[['LSTAT', 'RM']]
y = boston['MEDV']

model = FinalModel()
model.train_model(X, y)
model.save_model('final_model_v1.pkl')