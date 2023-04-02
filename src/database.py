import joblib


purchases_collection = joblib.load('./src/models/pkl/purchase_collection.pkl')
data_collection = joblib.load('./src/models/pkl/data_collection.pkl')
companies_collection = joblib.load('./src/models/pkl/companies_collection.pkl')
contracts_collection = joblib.load('./src/models/pkl/contracts_collection.pkl')


async def get_data_database():
    return data_collection


async def get_purchases_database():
    return purchases_collection


async def get_companies_database():
    return companies_collection


async def get_contracts_database():
    return contracts_collection


async def get_exact_id_data(exact_id: str):
    result = data_collection[data_collection['customer_inn'] == int(exact_id)]
    return result


async def get_exact_id_purchases(exact_id: str):
    result = purchases_collection[purchases_collection['customer_inn'] == int(exact_id)]
    return result


async def get_exact_id_contracts(exact_id: str):
    result = contracts_collection[contracts_collection['customerid": "purch_6123338"_inn'] == int(exact_id)]
    return result
