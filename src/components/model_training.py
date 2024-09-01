import os
import pickle
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler

class ModelTrainer:
    def __init__(self, file_path, target_column='avg_salary', test_size=0.2, random_state=42):
        self.file_path = file_path
        self.target_column = target_column
        self.test_size = test_size
        self.random_state = random_state
        self.model = RandomForestRegressor()
        self.scaler = StandardScaler()
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
    
    def load_data(self):
        """Loads the dataset from the file path."""
        self.df = pd.read_csv(self.file_path)
    
    def split_data(self):
        """Preprocesses the data by splitting it and scaling the features."""
        X = self.df.drop(self.target_column, axis=1)
        y = self.df[self.target_column]
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)
        self.X_train = self.scaler.fit_transform(self.X_train)
        self.X_test = self.scaler.transform(self.X_test)
    
    def train_model(self):
        """Trains the RandomForestRegressor model."""
        self.model.fit(self.X_train, self.y_train)
    
    def save_model(self, directory='artifacts', model_file='model_file.p', scaler_file='scaler_file.p'):
        """Saves the trained model to a file."""
        # Save model
        model_path = os.path.join(directory, model_file)
        with open(model_path, 'wb') as file:
            pickle.dump(self.model, file)
        
        # Save scaler
        scaler_path = os.path.join(directory, scaler_file)
        with open(scaler_path, 'wb') as file:
            pickle.dump(self.scaler, file)
    
    def run(self):
        """Runs the complete pipeline: load data, preprocess, train, and save model."""
        self.load_data()
        self.split_data()
        self.train_model()
        self.save_model()