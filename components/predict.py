import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler
import pandas as pd

class Predict:
    def __init__(self, model_path, scalar_path):
        self.model_file = model_path
        self.model = None
        self.scaler_file = scalar_path
        self.onehot_encoder = OneHotEncoder(sparse=False, drop='first')
        self.cat_features = ['Company Name', 'Location', 'Type of ownership', 'Industry', 'Sector', 'job_simp', 'seniority']
    
    def load_model(self):
        """Loads the trained model and scaler from files."""
        # Load model
        with open(self.model_file, 'rb') as file:
            self.model = pickle.load(file)
    
        # Load scaler
        with open(self.scaler_file, 'rb') as file:
            self.scaler = pickle.load(file)
    
    def preprocess(self, X):
        """Preprocesses the input data by one-hot encoding categorical features and scaling numeric features."""
        
        if not all(feature in X.columns for feature in self.cat_features):
            raise ValueError("Some categorical features are missing from the input data")
        encoded_features = self.onehot_encoder.fit_transform(X[self.cat_features])
        encoded_df = pd.DataFrame(encoded_features, columns=self.onehot_encoder.get_feature_names_out(self.cat_features))
        X_encoded = pd.concat([X.drop(columns=self.cat_features), encoded_df], axis=1)

        X_scaled = self.scaler.transform(X_encoded)
        
        return X_scaled

    def predict(self, X):
        """Predicts the target using the loaded model and scaler."""
        return self.model.predict(X)