import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
import os
import pickle
from scipy import stats
import numpy as np

class JobDataProcessor:
    def __init__(self):
        self.df = pd.read_csv("artifacts/data_clean.csv")
        self.onehot_encoder = OneHotEncoder(sparse_output=False)
        self.num_features = ['Rating', 'Age']
        self.cat_features = ['Company Name', 'Location', 'Ownership', 'Industry', 'Sector', 'job_simp', 'seniority','Revenue_Upper','Size_Upper']

    def convert_dtypes(self):
        """Converts boolean features to integer type."""
        for col in self.num_features:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')

        for col in self.cat_features:
            self.df[col] = self.df[col].astype('category')
    
    def fill_missing(self):
        """Fills missing values using SimpleImputer for numeric and categorical features."""
        # Impute numeric features with the mean
        num_imputer = SimpleImputer(strategy='mean')
        self.df[self.num_features] = num_imputer.fit_transform(self.df[self.num_features])
    
    def encode_categorical_features(self):
        """Encodes categorical features using OneHotEncoder."""
        encoded_features = self.onehot_encoder.fit_transform(self.df[self.cat_features])
        encoded_df = pd.DataFrame(encoded_features, columns=self.onehot_encoder.get_feature_names_out(self.cat_features))
        self.df = pd.concat([self.df.drop(columns=self.cat_features), encoded_df], axis=1)
    
    def outliers_log_transform(self):
        self.df['log_avg_salary'] = np.log(self.df['avg_salary'] + 1)
        z_scores = stats.zscore(self.df['log_avg_salary'])
        self.df = self.df[np.abs(z_scores) <= 2]
        self.df=self.df.drop('avg_salary',axis=1)

    def process_data(self):
        """Runs the full data preprocessing pipeline."""
        self.convert_dtypes()
        self.fill_missing()
        self.encode_categorical_features()
        self.outliers_log_transform()
    
    def save_data(self):
        """Saves the processed DataFrame to a CSV file."""
        directory = os.path.dirname("artifacts/data_transform.csv")
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.df.to_csv("artifacts/data_transform.csv", index=False)

        # Save encoder
        model_path = os.path.join('artifacts', "onehot_encoder.p")
        with open(model_path, 'wb') as file:
            pickle.dump(self.onehot_encoder, file)

if __name__=="__main__":
    job_data_processor = JobDataProcessor()
    job_data_processor.process_data()
    job_data_processor.save_data()