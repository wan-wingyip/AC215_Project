from flask import Flask, jsonify, request
import pandas as pd
import joblib

app = Flask(__name__)

model = joblib.load("final_model_v1.pkl") # change this name for the correct model

@app.route('/predict', methods = ["POST"])
def predict():
    data = request.get_json()
    df = pd.DataFrame()
    df["LSTAT"] = data["LSTAT"]
    df["RM"] = data["RM"]
    predictions = model.predict(df)
    return jsonify({'predictions': predictions.tolist()})

if __name__ == '__main__':
    app.run(host = '0.0.0.0', port = 8080)