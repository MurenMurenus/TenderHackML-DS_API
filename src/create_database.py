import pandas as pd
from pymongo import MongoClient

client = MongoClient('mongodb://root:rootpassword@192.168.247.252:27017')
db_raw = client['VendorDb']
collection = db_raw['data']
collection.drop()
data_pd = pd.read_csv('./data/data.csv')
data_pd.reset_index(inplace=True)
data_pd = data_pd.to_dict("records")
collection.insert_many(data_pd)
print('data filled')

collection = db_raw['purchases']
collection.drop()
data_pd = pd.read_csv('./data/purchases.csv')
data_pd.reset_index(inplace=True)
data_pd = data_pd.to_dict("records")
collection.insert_many(data_pd)
print('purchases filled')
