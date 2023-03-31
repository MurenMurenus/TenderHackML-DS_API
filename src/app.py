from flask import Flask

from src import controllers


# API definition
app = Flask(__name__)


@app.route('/api/predict/test_model', methods=['POST'])
async def predict():
    predictions = await controllers.async_predict()
    return predictions


@app.route('/api/metrics', methods=['POST'])
async def metrics():
    o_metrics = await controllers.get_metrics()
    return o_metrics
