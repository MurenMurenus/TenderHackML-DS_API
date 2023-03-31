import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
import joblib


# Load the dataset in a dataframe object and include only four features as mentioned
url = "https://s3.amazonaws.com/assets.datacamp.com/course/Kaggle/train.csv"
df = pd.read_csv(url)
include = ['Age', 'Sex', 'Embarked', 'Survived'] # Only four features
df_ = df[include]

# Data Preprocessing
categories = []
for col, col_type in df_.dtypes.iteritems():
     if col_type == 'O':
          categories.append(col)
     else:
          df_[col].fillna(0, inplace=True)

df_ohe = pd.get_dummies(df_, columns=categories, dummy_na=True)

# Logistic Regression classifier
dependent_variable = 'Survived'
x = df_ohe[df_ohe.columns.difference([dependent_variable])]
y = df_ohe[dependent_variable]
lr = LogisticRegression()
lr.fit(x, y)

# Save your model
joblib.dump(lr, 'model.pkl')
print("Model dumped successfully!")

# Load the model that you just saved
lr = joblib.load('model.pkl')

# Saving the data columns from training
model_columns = list(x.columns)
joblib.dump(model_columns, 'model_columns.pkl')
print("Models columns dumped successfully!")
