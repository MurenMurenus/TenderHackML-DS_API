import pandas as pd
from pymongo import MongoClient


async def get_data_database():
    client = MongoClient('mongodb://root:rootpassword@192.168.247.252:27017')
    db_raw = client['VendorDb']
    collection = db_raw['data']
    db = pd.DataFrame(collection.find())
    db = db.drop(axis=1, columns='_id')
    return db


async def get_purchases_database():
    client = MongoClient('mongodb://root:rootpassword@192.168.247.252:27017')
    db_raw = client['VendorDb']
    collection = db_raw['purchases']
    db = pd.DataFrame(collection.find())
    db = db.drop(axis=1, columns='_id')
    return db


async def get_exact_id_data(exact_id: str):
    db = await get_data_database()
    result = db[db['id']==exact_id]
    return result


async def get_exact_id_purchases(exact_id: str):
    db = await get_purchases_database()
    result = db[db['id']==exact_id]
    return result
