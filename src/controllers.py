import flask
from flask import request
import joblib
import json
import traceback
import pandas as pd
import numpy as np

from src.models import pipeline
import src.database as mongodb


lr = joblib.load("src/models/model.pkl")  # Load pkl of our model.
print('Model loaded')
model_columns = joblib.load("src/models/model_columns.pkl")  # Load columns that our model uses.
print('Model columns loaded')


async def get_all_purchases():
    result = await mongodb.get_data_database()
    print(result.head())
    out = result.head().to_json(orient='index')
    print(out)
    return out


async def get_exact():
    try:
        json_id = request.json
        print(json_id)
        exact_info = await mongodb.get_exact_id_data(json_id[id])
        out = exact_info.to_json(orient='index')
        return out

    except:
        return {'trace': traceback.format_exc()}


async def get_predictions():
    if lr:
        try:
            json_ = request.json
            print(json_)
            data = await pipeline.pipeline(pd.DataFrame([json_]))
            prediction = lr.predict(data)[0]

            return {'prediction': str(prediction)}

        except:
            return {'trace': traceback.format_exc()}
    else:
        print('Train the model first')
        return {'trace': str('Train the model first')}
