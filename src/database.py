import pandas as pd
from pymongo import MongoClient

IP = "192.168.1.50"

client = MongoClient(f'mongodb://root:rootpassword@{IP}:27017')
db_raw = client['VendorDb']
purchases_collection = pd.DataFrame(db_raw['purchases'].find()).drop(axis=1, columns='_id')
print('Purchases')
data_collection = pd.DataFrame(db_raw['data'].find()).drop(axis=1, columns='_id')
print('Data')

async def get_data_database():
    return data_collection


async def get_purchases_database():
    return purchases_collection


async def get_exact_id_data(exact_id: str):
    db = await get_data_database()
    result = db[db['id']==exact_id]
    return result


async def get_exact_id_purchases(exact_id: str):
    db = await get_purchases_database()
    result = db[db['id']==exact_id]
    return result
