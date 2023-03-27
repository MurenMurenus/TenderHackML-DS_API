# Dependencies
from flask import Flask, request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np


# Your API definition
app = Flask(__name__)
lr = joblib.load("src/models/model.pkl")  # Load "model.pkl"
print('Model loaded')
model_columns = joblib.load("src/models/model_columns.pkl")  # Load "model_columns.pkl"
print('Model columns loaded')


async def async_predict():
    global lr
    if lr:
        try:
            json_ = request.json
            print(json_)
            # for multiple predictions (already a list)
            # query = pd.get_dummies(pd.DataFrame(json_))

            # for a single prediction
            query = pd.get_dummies(pd.DataFrame([json_]))
            query = query.reindex(columns=model_columns, fill_value=0)

            # for multiple predictions at a time
            # prediction = list(lr.predict(query))

            # for a single prediction
            prediction = lr.predict(query)[0]

            return jsonify({'prediction': str(prediction)})

        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Train the model first')
        return 'No model here to use'


@app.route('/api/predict/test_model', methods=['POST'])
async def predict():
    predictions = await async_predict()
    return predictions
