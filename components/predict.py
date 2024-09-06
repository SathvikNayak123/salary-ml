import pickle
import numpy as np
from sklearn.preprocessing import OneHotEncoder
from components.data_transform import JobDataProcessor
import pandas as pd

class Predict:
    def __init__(self, model_path, scalar_path):
        self.model_file = model_path
        self.model = None
        self.scaler_file = scalar_path
        self.onehot_encoder = OneHotEncoder(sparse=False, drop='first')
        self.cat_features = ['Company Name', 'Location', 'Type of ownership', 'Industry', 'Sector', 'job_simp', 'seniority', 'Revenue_Upper', 'Size_Upper' ]
    
    def load_model(self):
        """Loads the trained model and scaler from files."""
        # Load model
        with open(self.model_file, 'rb') as file:
            self.model = pickle.load(file)
    
        # Load scaler
        with open(self.scaler_file, 'rb') as file:
            self.scaler = pickle.load(file)
    
    def predict(self, X):
        """Predicts the target using the loaded model and scaler."""
        X_std = self.scaler.transform(X)
        return self.model.predict(X_std)