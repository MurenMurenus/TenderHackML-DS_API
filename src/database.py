import pandas as pd
from pandas.io.json import json_normalize
from pymongo import MongoClient


def create_database():
    client = MongoClient('mongodb://root:rootpassword@192.168.1.50:27017')
    db_raw = client['VendorDb']
    collection = db_raw['data']
    collection.drop()
    data_pd = pd.read_csv('src/data/data.csv')
    print('read_csv completed')
    data_pd.reset_index(inplace=True)
    collection.insert_one({'shit1': 'shit2'})
    print('BD filled')


async def get_all_database():
    client = MongoClient('mongodb://root:rootpassword@192.168.1.50:27017')
    db_raw = client['VendorDb']
    collection = db_raw['data']
    db = pd.DataFrame(json_normalize(list(collection.find())))
    print(db)
    return db


async def get_exact_id(exact_id: str):
    db = get_all_database()
    result = db[db['id']==exact_id]
    return result
