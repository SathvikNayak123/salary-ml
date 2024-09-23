import os
import pickle
import pandas as pd
from sklearn.linear_model import ElasticNet
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import mean_squared_error, r2_score

class ModelTrainer:
    def __init__(self):
        self.target_column = 'log_avg_salary'
        self.test_size = 0.2
        self.random_state = 42
        self.model = ElasticNet(alpha=0.1, l1_ratio=0.1)
        self.scaler = StandardScaler()
        self.df = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        #numeric features to scale
        self.numeric_features = ['Rating', 'Age']
    
    def load_data(self):
        """Loads the dataset from the file path."""
        self.df = pd.read_csv("artifacts/data_transform.csv")
    
    def split_data(self):
        """Preprocesses the data by splitting it and scaling only the numeric features."""
        X = self.df.drop(self.target_column, axis=1)
        y = self.df[self.target_column]
        
        # Split the data into train and test sets
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=self.test_size, random_state=self.random_state)
        
        # Scale only the specified numeric features
        self.X_train[self.numeric_features] = self.scaler.fit_transform(self.X_train[self.numeric_features])
        self.X_test[self.numeric_features] = self.scaler.transform(self.X_test[self.numeric_features])
    
    def train_model(self):
        """Trains the RandomForestRegressor model."""
        self.model.fit(self.X_train, self.y_train)
    
    def evaluate_model(self):
        """Evaluates the model on the test set and prints metrics."""
        y_pred = self.model.predict(self.X_test)
        mse = mean_squared_error(self.y_test, y_pred)
        r2 = r2_score(self.y_test, y_pred)
        print(f"Model Evaluation:\nMean Squared Error: {mse}\nR^2 Score: {r2}")
    
    def save_model(self, directory='artifacts', model_file='model_file.p', scaler_file='scaler_file.p'):
        """Saves the trained model to a file."""
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        # Save model
        model_path = os.path.join(directory, model_file)
        with open(model_path, 'wb') as file:
            pickle.dump(self.model, file)
        
        # Save scaler
        scaler_path = os.path.join(directory, scaler_file)
        with open(scaler_path, 'wb') as file:
            pickle.dump(self.scaler, file)
    
    def run(self):
        """Runs the complete pipeline: load data, preprocess, train, evaluate, and save model."""
        self.load_data()
        self.split_data()
        self.train_model()
        #self.evaluate_model()
        self.save_model()

