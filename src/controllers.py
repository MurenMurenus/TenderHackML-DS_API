import flask
from flask import request, jsonify
import joblib
import traceback
import pandas as pd
import numpy as np

from src.models import pipeline


lr = joblib.load("src/models/model.pkl")  # Load pkl of our model.
print('Model loaded')
model_columns = joblib.load("src/models/model_columns.pkl")  # Load columns that our model uses.
print('Model columns loaded')


async def get_predictions() -> flask.Response:
    if lr:
        try:
            json_ = request.json
            print(json_)
            data = await pipeline.pipeline(pd.DataFrame([json_]))
            prediction = lr.predict(data)[0]

            return jsonify({'prediction': str(prediction)})

        except:
            return jsonify({'trace': traceback.format_exc()})
    else:
        print('Train the model first')
        return jsonify({'trace': str('Train the model first')})


async def get_metrics() -> flask.Response:
    try:
        json_ = request.json
        print(json_)
        data = pipeline.pipeline(pd.DataFrame([json_]))
        statistics = 'Test statistics'
        return jsonify({'metrics': str(statistics)})

    except:
        return jsonify({'trace': traceback.format_exc()})


async def get_efficiency() -> flask.Response:
    try:
        json_ = request.json
        print(json_)
        data = pipeline.pipeline(pd.DataFrame([json_]))
        efficiency = 1
        return jsonify({'efficiency': str(efficiency)})

    except:
        return jsonify({'trace': traceback.format_exc()})
