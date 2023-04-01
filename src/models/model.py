import joblib
import pandas as pd
import sklearn
from sklearn.linear_model import LinearRegression

my_id='purch_743865'
purch=pd.read_csv('/kaggle/input/tenderhack/purchases.csv',sep=';')
part=pd.read_csv('/kaggle/input/tenderhack/data.csv')
comp=pd.read_csv('/kaggle/input/tenderhack/companies.csv',sep=';')
#contracts=pd.read_csv('contracts.csv',sep=';')

all_data=part[part['id']==my_id]

if all_data.shape[0]>0:
    winned = all_data[all_data['is_winner']=='Да']
    #percent_winned
    percent_winned = (winned.shape[0]/all_data.shape[0])*100

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

    print(df)
    print(result_df)

    df_everyone = df
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

    joblib.dump(model, 'model.pkl')
