import pandas as pd
import joblib


model_columns = joblib.load("src/models/model_columns.pkl")  # Load columns that our model uses.


async def pipeline(input_dataframe: pd.DataFrame) -> pd.DataFrame:
    # interactions with data here
    data = pd.get_dummies(input_dataframe)
    data = data.reindex(columns=model_columns, fill_value=0)
    return data
