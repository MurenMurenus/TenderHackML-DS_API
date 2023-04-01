import pandas as pd
from pymongo import MongoClient

IP = '10.10.117.233'
client = MongoClient(f'mongodb://root:rootpassword@{IP}:27017')
db_raw = client['VendorDb']
# collection = db_raw['data']
# collection.drop()
# data_pd = pd.read_csv('./data/data.csv')
# data_pd.reset_index(inplace=True)
# data_pd = data_pd.to_dict("records")
# collection.insert_many(data_pd)
# print('data filled')

# collection = db_raw['purchases']
# collection.drop()
# purchases_pd = pd.read_csv('./data/purchases.csv', sep=';')
# purchases_pd.reset_index(inplace=True)
# purchases_pd = purchases_pd.to_dict("records")
# collection.insert_many(purchases_pd)
# print('purchases filled')

collection = db_raw['companies']
purchases_pd = pd.read_csv('./data/companies.csv', sep=';')
purchases_pd.reset_index(inplace=True)
purchases_pd = purchases_pd.to_dict("records")
collection.insert_many(purchases_pd)
print('companies filled')
