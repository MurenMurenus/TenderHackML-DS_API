from flask import Flask

from src import controllers
from src import metrics


# API definition
app = Flask(__name__)


@app.route('/api/get_exact_id', methods=['POST'])
async def exact_id():
    purchases = await controllers.get_exact()
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
