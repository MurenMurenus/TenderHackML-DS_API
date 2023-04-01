import json

import pandas as pd
from flask import request, jsonify

from src import database


async def get_contract_category():
    my_id = request.get_json(force=True)['id']

    all_data = await database.get_exact_id_data(my_id)
    purch = await database.get_exact_id_purchases(my_id)
    part = await database.get_data_database()
    if all_data.shape[0] > 0:
        winned = all_data[all_data['is_winner'] == 'Да']
        len_winned = winned.shape[0]
        # percent_ks
        percent_ks = winned[winned['contract_category'] == 'КС'].shape[0] / len_winned
        # percent_need
        percent_need = winned[winned['contract_category'] == 'Потребность'].shape[0] / len_winned
        return {"percent_ks": percent_ks, "percent_need": percent_need}
    else:
        print('No data about this user')
    # no data about this user


async def get_regional_stat():
    my_id = request.get_json(force=True)['id']

    all_data = await database.get_exact_id_data(my_id)
    if all_data.shape[0] > 0:
        winned = all_data[all_data['is_winner'] == 'Да']

        all_regions = winned['delivery_region'].unique()
        percent_region = {}
        len_winned = winned.shape[0]

        out = []
        for i in all_regions:
            cur_reg = winned[winned['delivery_region'] == i].shape[0]
            percent_region[i] = (cur_reg / len_winned) * 100
            out.append({'name': i, 'value': percent_region[i]})
        # percent_region

        print(out)
        return out
    else:
        print('No data about this user')
    # no data about this user


async def get_percent_won():
    my_id = request.get_json(force=True)['id']

    all_data = await database.get_exact_id_data(my_id)
    purch = await database.get_exact_id_purchases(my_id)
    part = await database.get_data_database()
    if all_data.shape[0] > 0:
        winned = all_data[all_data['is_winner'] == 'Да']
        # percent_winned
        percent_winned = (winned.shape[0] / all_data.shape[0]) * 100
        # total_price
        total_price = sum(winned['price'].values)

        all_regions = winned['delivery_region'].unique()
        percent_region = {}
        len_winned = winned.shape[0]

        for i in all_regions:
            cur_reg = winned[winned['delivery_region'] == i].shape[0]
            percent_region[i] = (cur_reg / len_winned) * 100
        # percent_region
        # percent_ks
        percent_ks = winned[winned['contract_category'] == 'КС'].shape[0] / len_winned
        # percent_need
        percent_need = winned[winned['contract_category'] == 'Потребность'].shape[0] / len_winned

        purchases = purch

        # Convert publish_date to datetime
        purchases['publish_date'] = pd.to_datetime(purchases['publish_date'])

        # Extract year-month from publish_date
        purchases['year_month'] = purchases['publish_date'].dt.strftime('%Y-%m')

        # Merge purchases and participants
        merged_data = purchases.join(part, lsuffix="DROP").filter(regex="^(?!.*DROP)")

        # Calculate winning percentage by year-month
        winners_by_year_month = merged_data[merged_data['is_winner'] == 'Да'].groupby('year_month').size()
        total_by_year_month = merged_data.groupby('year_month').size()
        # everyone stat
        percent_won_by_year_month = (winners_by_year_month / total_by_year_month) * 100

        id_data = merged_data[merged_data['id'] == my_id]

        # Calculate winning percentage by year-month for my_id
        winners_by_year_month = id_data[id_data['is_winner'] == 'Да'].groupby('year_month').size()
        total_by_year_month = id_data.groupby('year_month').size()
        percent_won_by_year_month = (winners_by_year_month / total_by_year_month) * 100

        # Create DataFrame with winning percentages for my_id
        result_df = pd.DataFrame(
            {'year_month': percent_won_by_year_month.index, 'winning_percentage': percent_won_by_year_month.values})
        print(result_df.to_json())
        return result_df.to_json()
    else:
        print('No data about this user')
    # no data about this user