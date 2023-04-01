import flask
from flask import Flask, request, jsonify

from src import controllers
from src import metrics

from flask_cors import CORS, cross_origin
app = Flask(__name__)
cors = CORS(app, resources={r'/api/*': {'origins': 'http://localhost:5173'}})
app.config['CORS_HEADERS'] = 'Content-Type'
# API definition


@app.route('/api/get_exact_id_data', methods=['POST'])
async def exact_id_data():
    data = await controllers.get_exact_data()
    return data


@app.route('/api/get_exact_id_purchases', methods=['POST'])
async def exact_id_purchases():
    purchases = await controllers.get_exact_purchases()
    return purchases


@app.route('/api/get_all_purchases', methods=['POST'])
async def all_purchases():
    purchases = await controllers.get_all_purchases()
    return purchases


@app.route('/api/predict/next', methods=['POST'])
async def predict():
    predictions = await controllers.get_predictions()
    return predictions


@app.route('/api/barChart', methods=['POST'])
async def categorical_method():
    percent = await metrics.get_contract_category()
    return percent


@app.route('/api/pieChart', methods=['POST'])
async def regional_method():
    regional = await metrics.get_regional_stat()
    response = flask.jsonify({"data": regional})
    # response.headers.add('Access-Control-Allow-Origin', '*')
    print(response.headers)
    return regional
