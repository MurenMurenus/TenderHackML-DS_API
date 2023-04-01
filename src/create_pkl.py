import pandas as pd
from pymongo import MongoClient
import joblib


IP = "10.10.117.233"

client = MongoClient(f'mongodb://root:rootpassword@{IP}:27017')
db_raw = client['VendorDb']
# purchases_collection = pd.DataFrame(db_raw['purchases'].find()).drop(axis=1, columns='_id')
# joblib.dump(purchases_collection, 'purchase_collection.pkl')
# print('Purchases')
# data_collection = pd.DataFrame(db_raw['data'].find()).drop(axis=1, columns='_id')
# joblib.dump(data_collection, 'data_collection.pkl')
# print('Data')

data_collection = pd.DataFrame(db_raw['companies'].find()).drop(axis=1, columns='_id')
joblib.dump(data_collection, 'pkls/companies_collection.pkl')
print('Companies')
