import os
import pickle
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

df=pd.read_csv('artifacts/data_transformed.csv')

X = df.drop('avg_salary', axis =1)
y = df['avg_salary']

model = RandomForestRegressor()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

model.fit(X_train, y_train)

directory = "artifacts"
file_path = os.path.join(directory, 'model_file.p')

model_data = {'model': model}
with open(file_path, 'wb') as file:
    pickle.dump(model_data, file)
