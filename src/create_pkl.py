import pandas as pd
from pymongo import MongoClient
import joblib


IP = "192.168.1.50"

client = MongoClient(f'mongodb://root:rootpassword@{IP}:27017')
db_raw = client['VendorDb']
# purchases_collection = pd.DataFrame(db_raw['purchases'].find()).drop(axis=1, columns='_id')
# print(purchases_collection.columns)
# #purchases_collection = purchases_collection.drop(axis=1, columns='Unnamed: 0')
# joblib.dump(purchases_collection, 'models/pkl/purchase_collection.pkl')
# print('Purchases')
# data_collection = pd.DataFrame(db_raw['data'].find()).drop(axis=1, columns='_id')
# print(data_collection.columns)
# data_collection = data_collection.drop(axis=1, columns='Unnamed: 0')
# joblib.dump(data_collection, 'models/pkl/data_collection.pkl')
# print('Data')
#
# data_collection = pd.DataFrame(db_raw['companies'].find()).drop(axis=1, columns='_id')
# print(data_collection.columns)
# #data_collection = data_collection.drop(axis=1, columns='Unnamed: 0')
# joblib.dump(data_collection, 'models/pkl/companies_collection.pkl')
# print('Companies')

data_collection = pd.DataFrame(db_raw['contracts'].find()).drop(axis=1, columns='_id')
print(data_collection.columns)
#data_collection = data_collection.drop(axis=1, columns='Unnamed: 0')
joblib.dump(data_collection, './pkl/contracts_collection.pkl')
print('Contracts')
