import flask
from flask import request
import joblib
import json
import traceback
import pandas as pd
import numpy as np

from src.models import pipeline
from src import database


lr = joblib.load("src/models/model.pkl")  # Load pkl of our model.
print('Model loaded')


async def get_all_purchases():
    result = await database.get_data_database()
    out = result.to_json(orient='index')
    print(out)
    return out


async def get_exact_data():
    try:
        json_id = request.get_json(force=True)
        print(json_id)
        exact_info = await database.get_exact_id_data(json_id['id'])
        out = exact_info.to_json(orient='index')
        return out

    except:
        return {'trace': traceback.format_exc()}


async def get_exact_purchases():
    try:
        json_id = request.get_json(force=True)
        print(json_id)
        exact_info = await database.get_exact_id_purchases(json_id['id'])
        out = exact_info.to_json(orient='index')
        return out

    except:
        return {'trace': traceback.format_exc()}


async def get_predictions():
    if lr:
        try:
            my_id = request.get_json(force=True)
            print(my_id)
            all_data = await database.get_exact_id_data(my_id)
            purch = await database.get_exact_id_purchases(my_id)
            part = await database.get_data_database()
            comp = pd.read_csv('/kaggle/input/tenderhack/companies.csv', sep=';')
            winned = all_data[all_data['is_winner'] == 'Да']
            # percent_winned
            percent_winned = (winned.shape[0] / all_data.shape[0]) * 100
            companies = comp[comp["status"] == 'Активная']
            print(part.columns.tolist())
            purchases = part.merge(companies, on='supplier_inn')
            # Convert publish_date to datetime
            purchases['publish_date'] = pd.to_datetime(purchases['publish_date'])

            # Extract year-month from publish_date
            purchases['year_month'] = purchases['publish_date'].dt.strftime('%Y-%m')

            # Merge purchases and participants
            merged_data = purchases
            # Calculate winning percentage by year-month
            winners_by_year_month = merged_data[merged_data['is_winner'] == 'Да'].groupby('year_month').size()
            total_by_year_month = merged_data.groupby('year_month').size()
            # everyone stat
            percent_won_by_year_month = (winners_by_year_month / total_by_year_month) * 100

            df = percent_won_by_year_month.reset_index(name='winning_percentage')
            df.columns = ['year_month', 'winning_percentage']
            id_data = merged_data[merged_data['id'] == my_id]

            # Calculate winning percentage by year-month for my_id
            winners_by_year_month = id_data[id_data['is_winner'] == 'Да'].groupby('year_month').size()

            total_by_year_month = id_data.groupby('year_month').size()
            print(total_by_year_month)
            percent_won_by_year_month = (winners_by_year_month.shape[0] / total_by_year_month) * 100

            # Create DataFrame with winning percentages for my_id
            result_df = pd.DataFrame(
                {'year_month': percent_won_by_year_month.index, 'winning_percentage': percent_won_by_year_month.values})
            df_everyone = df
            # Convert year_month column to datetime format if necessary
            df_everyone['year_month'] = pd.to_datetime(df_everyone['year_month'])
            predicted_percentage = lr.predict(all_data)[0]
            new_row = pd.DataFrame({"year_month": [df_everyone['year_month'].max() + pd.DateOffset(months=1)],
                                    "winning_percentage": [predicted_percentage[0]]})
            return new_row.to_json(orient='index')

        except:
            return {'trace': traceback.format_exc()}
    else:
        print('Train the model first')
        return {'trace': str('Train the model first')}
