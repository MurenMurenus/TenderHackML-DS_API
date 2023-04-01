from flask import Flask

from src import controllers
from src import metrics


# API definition
app = Flask(__name__)


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


@app.route('/api/predict/test_model', methods=['POST'])
async def predict():
    predictions = await controllers.get_predictions()
    return predictions


@app.route('/api/get_percent_won', methods=['POST'])
async def percent_method():
    percent = await metrics.get_percent_won()
    return percent


@app.route('/api/pieChart', methods=['POST'])
async def regional_method():
    regional = await metrics.get_regional_stat()
    return regional
