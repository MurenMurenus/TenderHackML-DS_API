import flask
from flask import Flask, request
from pymongo import MongoClient

from src import controllers
from src import metrics

from flask_cors import CORS, cross_origin

from src.controllers import get_exact

app = Flask(__name__)
cors = CORS(app, resources={r'/api/*': {'origins': 'http://localhost:5173'}})
app.config['CORS_HEADERS'] = 'Content-Type'
# API definition


@app.route('/api/sth', methods=['POST'])
async def sth():
    IP = "192.168.1.50"
    client = MongoClient(f'mongodb://root:rootpassword@{IP}:27017')
    db_raw = client['VendorDb']
    data = db_raw['data'].find_one({"id": request.get_json(force=True)['id']})
    data['_id'] = 0

    return data


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

    return {'Total income now': o_income[0], 'Total income prev': o_income[1]}


@app.route('/api/region_statistics', methods=['POST'])
async def get_stat_region():
    my_id = request.get_json(force=True)['id']
    out = await metrics.get_whole_region_stats(my_id)

    return out


@app.route('/api/statistics', methods=['POST'])
async def get_stat_income():
    json_ = request.get_json(force=True)
    my_id = json_['id']
    fr = json_['from']
    to = json_['to']
    o_income = await metrics.income(my_id, fr, to)
    regions = (await metrics.get_top_region(fr, to, my_id)).sort_values(by='price_y')

    return {'Total income now': o_income[0], 'Total income prev': o_income[1], 'Regions': regions.to_json()}


@app.route('/api/get_exact_id_purchases', methods=['POST'])
async def exact_id_purchases():
    purchases = await controllers.get_exact_purchases()

    return purchases


@app.route('/api/get_exact_id_data', methods=['POST'])
async def exact_id_data():
    purchases = await controllers.get_exact_data()

    return purchases


@app.route('/api/curve', methods=['POST'])
async def curve():
    my_id = request.get_json(force=True)['id']
    predictions = await controllers.get_curve(my_id)

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

    return regional
