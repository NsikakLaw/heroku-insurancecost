from flask import Flask,request, url_for, redirect, render_template, jsonify
from sklearn.externals import joblib 
import pandas as pd
import numpy as np

app = Flask(__name__)

model = joblib.load('insurance_predictor.pkl')
data_columns = ['age', 'sex', 'bmi', 'children', 'smoker', 'region']

@app.route('/')
def home():
    return render_template("home.html")

@app.route('/predict',methods=['POST'])
def predict():
    int_features = [x for x in request.form.values()]
    final = np.array(int_features)
    new_data = pd.DataFrame([final], columns = data_columns)
    prediction = model.predict(new_data)
    return render_template('home.html',pred='Your Predicted Insurance Bill will be {}'.format(prediction))

@app.route('/predict_api',methods=['POST'])
def predict_api():
    data = request.get_json(force=True)
    new_data = pd.DataFrame([data])
    prediction = model.predict(new_data)
    output = prediction.Label[0]
    return jsonify(output)

if __name__ == '__main__':
    app.run(debug=True)