import flask
from flask import request
import joblib
import json
import traceback
import pandas as pd
from datetime import datetime

from src import database
from src import metrics
from pymongo import MongoClient


async def get_by_timestamp(from_: str, to: str, inn_: str) -> list[[dict]]:
    IP = '192.168.222.252'
    client = MongoClient(f'mongodb://root:rootpassword@{IP}:27017')
    db_raw = client['VendorDb']
    data = db_raw['contracts'].find({'customer_inn': int(inn_)})  # request.get_json(force=True)['id']})

    date_from = datetime.strptime(from_,"%Y-%m-%d")
    date_to = datetime.strptime(to, "%Y-%m-%d")
    prev = datetime.strptime(from_, "%Y-%m-%d") - pd.DateOffset(months=1)
    out = [[], []]

    for elem in data:
        x = elem
        if date_from <= datetime.strptime(x['contract_conclusion_date'], "%Y-%m-%d") <= date_to:
            out[0].append(x)
        elif prev <= datetime.strptime(x['contract_conclusion_date'], "%Y-%m-%d") <= date_from:
            out[1].append(x)

    for each in out[0]:
        each['_id'] = 0
    for each in out[1]:
        each['_id'] = 0

    return out


async def get_exact():
    IP = "192.168.222.252"
    client = MongoClient(f'mongodb://root:rootpassword@{IP}:27017')
    db_raw = client['VendorDb']

    return db_raw['data'].find_one({"_inn": request.get_json(force=True)['customer_inn']})


async def get_all_purchases():
    result = await database.get_data_database()
    out = result.to_json(orient='index', force_ascii=False)

    return out


async def get_exact_data():
    try:
        json_id = request.get_json(force=True)
        exact_info = await database.get_exact_id_data(json_id['customer_inn'])
        out = exact_info.to_json(orient='index', force_ascii=False)

        return out

    except:
        return {'trace': traceback.format_exc()}


async def get_exact_purchases():
    try:
        json_id = request.get_json(force=True)
        print(json_id)
        exact_info = await database.get_exact_id_purchases(json_id['customer_inn'])
        out = exact_info.to_json(orient='index', force_ascii=False)

        return out

    except:
        return {'trace': traceback.format_exc()}


async def get_exact_companies():
    try:
        json_id = request.get_json(force=True)
        print(json_id)
        exact_info = await database.get_exact_id_purchases(json_id['customer_inn'])
        out = exact_info.to_json(orient='index', force_ascii=False)

        return out

    except:
        return {'trace': traceback.format_exc()}


async def get_curve(my_inn):
    print(2)
    contracts = joblib.load('./src/models/pkl/contracts_collection.pkl')
    all_data = await database.get_data_database()
    data_winned_all = \
        all_data[all_data['is_winner'] == 'Да'].drop('Unnamed: 0', axis=1).\
            drop('delivery_region', axis=1).drop('lot_name', axis=1).\
            drop('customer_inn', axis=1)

    contracts_full_data = data_winned_all.merge(contracts, on='id')
    contracts_full_data = contracts_full_data.loc[contracts_full_data['price_x'] >= contracts_full_data['price_y']]

    top_reg = (await metrics.get_top_region("1970-01-01", "2100-01-01", my_inn)).head(1)['delivery_region']
    print(top_reg)
    my_region = top_reg[0]
    my_lots = contracts_full_data[contracts_full_data['customer_inn'] == int(my_inn)]
    my_lots = my_lots.groupby('lot_name')['price_y'].sum().reset_index()
    my_lot_name = list((my_lots[['lot_name', 'price_y']].sort_values(by='price_y', ascending=False)).head(1)['lot_name'].values)[0]
    print(my_lot_name)

    # boolean indexing to extract rows that match your criteria
    mask = (contracts_full_data['customer_inn'] == int(my_inn)) & \
           (contracts_full_data['delivery_region'] == my_region) & \
           (contracts_full_data['lot_name'] == my_lot_name)

    selected_rows_id = contracts_full_data[mask]
    print(selected_rows_id.head())
    # assuming selected_rows is your DataFrame containing the selected rows

    # if you want to sort in descending order, use the argument ascending=False
    sorted_rows = selected_rows_id.sort_values(by='contract_conclusion_date', ascending=True)
    sorted_rows_id = sorted_rows[['price_y', 'contract_conclusion_date']]
    out = [[], []]
    sorted_rows_id = sorted_rows_id.to_dict()
    print(sorted_rows_id)

    for k in sorted_rows_id['price_y'].keys():
        out[0].append({'price': sorted_rows_id['price_y'][k],
                       'contract_conclusion_date': sorted_rows_id['contract_conclusion_date'][k]})
    print(out[0])
    # sorted_rows_id.to_csv('id_mean.csv', index=False)

    # filter by region and lot name
    df_filtered = contracts_full_data[
        (contracts_full_data['delivery_region'] == my_region) & (contracts_full_data['lot_name'] == my_lot_name)]

    # convert 'publish_date' to datetime
    df_filtered['contract_conclusion_date'] = pd.to_datetime(df_filtered['contract_conclusion_date'])
    mean_prices = df_filtered[['contract_conclusion_date', 'price_y']]
    mean_prices = mean_prices.sort_values(by='contract_conclusion_date', ascending=True)
    mean_prices = mean_prices.to_dict()
    print(mean_prices)
    for k in mean_prices['price_y'].keys():
        out[1].append({'price': mean_prices['price_y'][k],
                       'contract_conclusion_date': str(mean_prices['contract_conclusion_date'][k])[:10]})
    print(out[1])
    # mean_prices.to_csv('all_mean.csv', index=False)

    return out
