# ML_API

API from a machine learning model in Python to get predictions with HTTP requests.
API is asynchronical, so it's possible to get requests from different client at the same time.

The model is dumped to .pkl file to be loaded in Flask API.
Features to check for predictions are dumped to .pkl file too, to protect data preprocessing of hidden bugs.
