import pickle
import pandas as pd

class Predict:
    def __init__(self, encoder_path, model_path, scalar_path):
        self.model_file = model_path
        self.encoder_file = encoder_path
        self.scaler_file = scalar_path
        self.expected_features = pd.read_csv("artifacts/data_transform.csv").drop('log_avg_salary',axis=1).columns
        self.cat_features = ['Company Name', 'Location', 'Ownership', 'Industry', 'Sector', 'job_simp', 'seniority', 'Revenue_Upper', 'Size_Upper' ]
        self.num_features = ['Rating','Age']
    
    def load_all(self):
        """Loads the trained model and scaler from files."""
        # Load encoder
        with open(self.encoder_file, 'rb') as file:
            self.encoder = pickle.load(file)

        # Load model
        with open(self.model_file, 'rb') as file:
            self.model = pickle.load(file)
    
        # Load scaler
        with open(self.scaler_file, 'rb') as file:
            self.scaler = pickle.load(file)

    def preprocess(self, X):
        """Preprocesses the input data: encodes categorical features and scales numerical features."""

        encoded_features = self.encoder.transform(X[self.cat_features])
        encoded_df = pd.DataFrame(encoded_features, columns=self.encoder.get_feature_names_out(self.cat_features))
        X = pd.concat([X.drop(columns=self.cat_features), encoded_df], axis=1)

        #X_new = X.reindex(columns=self.expected_features, fill_value=0)

        X[self.num_features] = self.scaler.transform(X[self.num_features])

        return X
    
    def predict(self, X):
        """Predicts the target using the loaded model."""
        return self.model.predict(X)