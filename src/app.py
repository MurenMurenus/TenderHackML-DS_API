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


@app.route('/api/metrics', methods=['POST'])
async def metrics_method():
    o_metrics = await metrics.get_metrics()
    return o_metrics
