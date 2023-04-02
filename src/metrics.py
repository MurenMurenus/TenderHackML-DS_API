import pandas as pd
from flask import request

from src import database
from src import controllers


async def income(my_inn, fr, to):
    contracts_full_data = await controllers.get_by_timestamp(fr, to, my_inn)

    out_now = 0
    for i in contracts_full_data[0]:
        out_now += i['price_y']
    out_prev = 0
    for i in contracts_full_data[1]:
        out_prev += i['price_y']
    return [out_now, out_prev]


async def get_contract_category():
    my_inn = request.get_json(force=True)['customer_inn']

    all_data = await database.get_exact_id_data(my_inn)

    if all_data.shape[0] > 0:
        winned = all_data[all_data['is_winner'] == 'Да']
        len_winned = winned.shape[0]
        # percent_ks
        percent_ks = winned[winned['contract_category'] == 'КС'].shape[0] / len_winned
        # percent_need
        percent_need = winned[winned['contract_category'] == 'Потребность'].shape[0] / len_winned

        return [
                    {"name": "Категории контрактов", "Котировочная сессия": percent_ks * 100, "Потребность": percent_need * 100, "amt": 0}
                ]
    else:
        print('No data about this user')
    # no data about this user


async def get_regional_stat():
    my_inn = request.get_json(force=True)['customer_inn']

    all_data = await database.get_exact_id_data(my_inn)
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

        return out
    else:
        print('No data about this user')
    # no data about this user


async def get_whole_region_stats(my_inn):
    most_frequent = pd.read_csv('src/data/most_frequent_lot_name_in_region.csv')
    number_of_companies = pd.read_csv('src/data/number_of_companies_all_regions.csv')
    number_lot_names = pd.read_csv('src/data/number_region_lot_name.csv')

    top_reg = (await get_top_region("1970-01-01", "2100-01-01", my_inn)).head(1)['delivery_region']

    lots = number_lot_names[number_lot_names['delivery_region'] == top_reg[0]]
    lots = (lots[['lot_name', 'count']].sort_values(by='count', ascending=False)).head(5)
    out1 = []
    most_frequent = most_frequent[most_frequent['delivery_region'] == top_reg[0]]
    for k in most_frequent['lot_name'].keys():
        out1.append({"Lot": str(most_frequent['lot_name'][k]), "Count": str(most_frequent['count'][k])})

    out_companies = number_of_companies[number_of_companies['delivery_region'] == top_reg[0]]
    print(out_companies)
    out2 = []
    for k in out_companies['delivery_region'].keys():
        out2.append({'region': out_companies['delivery_region'][k],
                     'companies': str(out_companies['id'][k])})

    out3 = []
    print(lots)
    for k in lots['lot_name'].keys():
        out3.append({"category": lots['lot_name'][k], "value": str(lots['count'][k])})

    # print the result
    return {"most_frequent_category": out1,
            "number_of_companies_on_region": out2,
            "lots_count_in_region": out3}


async def get_top_region(from_, to, inn_):
    contracts_full_data = pd.DataFrame((await controllers.get_by_timestamp(from_, to, inn_))[0])
    print(contracts_full_data.columns)
    print('groupby')
    vals = contracts_full_data.groupby('delivery_region')['price_y'].sum().reset_index()

    return vals


async def get_percent_won():
    my_inn = request.get_json(force=True)['customer_inn']

    all_data = await database.get_exact_id_data(my_inn)
    purch = await database.get_exact_id_purchases(my_inn)
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

        id_data = merged_data[merged_data['customer_inn'] == int(my_inn)]

        # Calculate winning percentage by year-month for my_id
        winners_by_year_month = id_data[id_data['is_winner'] == 'Да'].groupby('year_month').size()
        total_by_year_month = id_data.groupby('year_month').size()
        percent_won_by_year_month = (winners_by_year_month / total_by_year_month) * 100

        # Create DataFrame with winning percentages for my_id
        result_df = pd.DataFrame(
            {'year_month': percent_won_by_year_month.index, 'winning_percentage': percent_won_by_year_month.values})

        return result_df.to_json(force_ascii=False)
    else:
        print('No data about this user')
    # no data about this user
