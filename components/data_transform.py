import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
import os
import pickle

class JobDataProcessor:
    def __init__(self):
        self.df = pd.read_csv("artifacts/data_clean.csv")
        self.onehot_encoder = OneHotEncoder(sparse_output=False)
        self.num_features = ['Rating', 'Age', 'desc_len']
        self.cat_features = ['Company Name', 'Location', 'Type of ownership', 'Industry', 'Sector', 'job_simp', 'seniority', 'Revenue_Upper', 'Size_Upper' ]

    def fill_missing(self):
        """Fills missing values using SimpleImputer for numeric and categorical features."""
        # Impute numeric features with the mean
        num_imputer = SimpleImputer(strategy='mean')
        self.df[self.num_features] = num_imputer.fit_transform(self.df[self.num_features])
        
        # Impute categorical features
        cat_imputer = SimpleImputer(strategy='most_frequent')
        self.df[self.cat_features] = cat_imputer.fit_transform(self.df[self.cat_features])
    
    def encode_categorical_features(self):
        """Encodes categorical features using OneHotEncoder."""
        encoded_features = self.onehot_encoder.fit_transform(self.df[self.cat_features])
        encoded_df = pd.DataFrame(encoded_features, columns=self.onehot_encoder.get_feature_names_out(self.cat_features))
        self.df = pd.concat([self.df.drop(columns=self.cat_features), encoded_df], axis=1)
    
    def convert_bool_to_int(self):
        """Converts boolean features to integer type."""
        for col in self.df.columns:
            if self.df[col].dtype == bool:
                self.df[col] = self.df[col].astype(int)

    def process_data(self):
        """Runs the full data preprocessing pipeline."""
        self.convert_bool_to_int()
        self.fill_missing()
        self.encode_categorical_features()
        
    
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