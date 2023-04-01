import flask
from flask import Flask, request, jsonify
from pymongo import MongoClient

from src import controllers
from src import metrics

from flask_cors import CORS, cross_origin

from src.controllers import get_exact

app = Flask(__name__)
cors = CORS(app, resources={r'/api/*': {'origins': 'http://localhost:5173'}})
app.config['CORS_HEADERS'] = 'Content-Type'
# API definition


@app.route('/api/get_exact_id', methods=['POST'])
async def exact_id():
    return get_exact()


@app.route('/api/income', methods=['POST'])
async def id_income():
    json_ = request.get_json(force=True)
    my_id = json_['id']
    fr = json_['from']
    to = json_['to']
    o_income = await metrics.income(my_id, fr, to)
    return {'Total income': o_income[my_id]}


@app.route('/api/top_region', methods=['POST'])
async def get_top_reg():
    purchases = await metrics.get_top_region()
    return {'Top region': purchases}


@app.route('/api/get_exact_id_purchases', methods=['POST'])
async def exact_id_purchases():
    purchases = await controllers.get_exact_purchases()
    return purchases


@app.route('/api/get_exact_id_data', methods=['POST'])
async def exact_id_data():
    purchases = await controllers.get_exact_data()
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
