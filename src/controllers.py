import flask
from flask import request
import joblib
import json
import traceback
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

from src.models import pipeline
from src import database
from pymongo import MongoClient


lr = joblib.load("./src/models/pkl/model.pkl")  # Load pkl of our model.
print('Model loaded')


async def get_exact():
    IP = "10.10.117.233"
    client = MongoClient(f'mongodb://root:rootpassword@{IP}:27017')
    db_raw = client['VendorDb']
    return db_raw['data'].find_one({"_id": request.get_json(force=True)['id']})


async def get_all_purchases():
    result = await database.get_data_database()
    out = result.to_json(orient='index')
    print(out)
    return out


async def get_exact_data():
    try:
        json_id = request.get_json(force=True)
        print(json_id['id'])
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


async def get_exact_companies():
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
            my_id = request.get_json(force=True)['id']
            print(my_id)
            all_data = await database.get_exact_id_data(my_id)
            purch = await database.get_exact_id_purchases(my_id)
            part = await database.get_data_database()
            comp = await database.get_companies_database()

            winned = all_data[all_data['is_winner'] == 'Да']
            print(winned)
            # percent_winned
            percent_winned = (winned.shape[0] / all_data.shape[0]) * 100

            companies = comp[comp["status"] == 'Активная']
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
            print(percent_won_by_year_month)

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
            test = df_everyone[-1:]['year_month'].values.reshape(-1, 1)
            test = pd.to_numeric(test.flatten()).reshape(-1, 1)
            predicted_percentage = lr.predict(test)
            new_row = pd.DataFrame({"year_month": [df_everyone['year_month'].max() + pd.DateOffset(months=1)],
                                    "winning_percentage": [predicted_percentage[0]]})
            all_predict = df.append(new_row, ignore_index=True)

            df_exact = result_df
            df_exact['year_month'] = pd.to_datetime(df_exact['year_month'])
            last_month = df_exact['year_month'].max()
            next_month = last_month + pd.DateOffset(months=1)
            new_row = pd.DataFrame({'year_month': [next_month],
                                    'winning_percentage': [0]})
            df_exact = df_exact.append(new_row, ignore_index=True)

            df_exact['year_month'] = pd.to_datetime(df_exact['year_month'])

            # Create training data by selecting all rows except the last one
            train_X = df_exact[:-1]['year_month'].values.reshape(-1, 1)
            train_y = df_exact[:-1]['winning_percentage']

            # Create test data by selecting the last row
            test_X = df_exact[-1:]['year_month'].values.reshape(-1, 1)
            test_X = pd.to_numeric(test_X.flatten()).reshape(-1, 1)
            # Initialize a linear regression model
            model = LinearRegression()

            # Train the model on the training data
            model.fit(train_X, train_y)

            # Predict the percentage for the next month
            predicted_percentage = model.predict(test_X)

            new_row = pd.DataFrame({"year_month": [next_month],
                                    "winning_percentage": [predicted_percentage[0]]})

            while next_month != df_everyone['year_month'].max():
                last_month = df_exact['year_month'].max()

                # Get the next month
                next_month = last_month + pd.DateOffset(months=1)
                new_row = pd.DataFrame({'year_month': [next_month],
                                        'winning_percentage': [0]})

                # Append the new row to the existing DataFrame
                df_exact = df_exact.append(new_row, ignore_index=True)

            # Print the output data frame

            output_df_exact = result_df.append(new_row, ignore_index=True)
            print(output_df_exact)

            contracts[contracts['id']==my_id]
            final_prices=contracts[contracts['id']==my_id]['price']
            start_prices=all_data[all_data['is_winner']=='Да']['price']
            diff=[]
            for i in range(len(start_prices.values)):
                d=final_prices.values[i]-start_prices.values[i]
                per=(d/start_prices.values[i])*100
                diff.append(per)

            f_everyone = df
            # Convert year_month column to datetime format if necessary
            df_everyone['year_month'] = pd.to_datetime(df_everyone['year_month'])

            # Create training data by selecting all rows except the last one
            train_X = df_everyone[:-1]['year_month'].values.reshape(-1, 1)
            train_y = df_everyone[:-1]['winning_percentage']

            # Create test data by selecting the last row
            test_X = df_everyone[-1:]['year_month'].values.reshape(-1, 1)
            test_X = pd.to_numeric(test_X.flatten()).reshape(-1, 1)
            # Initialize a linear regression model
            model = LinearRegression()

            # Train the model on the training data
            model.fit(train_X, train_y)

            # Predict the percentage for the next month
            predicted_percentage = model.predict(test_X)

            new_row = pd.DataFrame({"year_month": [df_everyone['year_month'].max() + pd.DateOffset(months=1)],
                                    "winning_percentage": [predicted_percentage[0]]})

            # Print the output data frame

            output_df = df.append(new_row, ignore_index=True)
            print(output_df)

            return output_df.to_json(orient='index')

        except:
            return {'trace': traceback.format_exc()}
    else:
        print('Train the model first')
        return {'trace': str('Train the model first')}
