import pandas as pd
import joblib


async def pipeline(input_dataframe: pd.DataFrame) -> pd.DataFrame:
    # interactions with data here
    data = pd.get_dummies(input_dataframe)
    return data
