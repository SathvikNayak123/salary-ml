import pandas as pd
from sklearn.preprocessing import OneHotEncoder

class JobDataProcessor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.df = pd.read_csv(file_path)
        self.num_features = ['Rating', 'avg_salary', 'ml_yn', 'dl_yn', 'ai_yn', 'python_yn', 'sql_yn', 'tool_yn', 'cloud_yn', 'Size_Upper', 'Age', 'Revenue_Upper', 'desc_len']
        self.cat_features = ['Company Name', 'Location', 'Type of ownership', 'Industry', 'Sector', 'job_simp', 'seniority']
    
    def calculate_description_length(self):
        """Calculates the length of job descriptions."""
        self.df['desc_len'] = self.df['Job Description'].apply(lambda x: len(x))
    
    def fill_missing(self):
        """Converts numeric features to numeric dtype and categorical features to category dtype."""
        for col in self.num_features:
            self.df[col] = pd.to_numeric(self.df[col], errors='coerce')
            self.df[col].fillna(self.df[col].mean(), inplace=True)
        for col in self.cat_features:
            self.df[col].fillna('Unknown', inplace=True)
            self.df[col] = self.df[col].astype('category')

    
    def drop_unnecessary_columns(self):
        """Drops unnecessary columns."""
        self.df = self.df.drop(['Job Title', 'Salary Estimate', 'Job Description'], axis=1)
    
    def encode_categorical_features(self):
        """Encodes categorical features using OneHotEncoder."""
        onehot_encoder = OneHotEncoder(sparse=False, drop='first')
        encoded_features = onehot_encoder.fit_transform(self.df[self.cat_features])
        encoded_df = pd.DataFrame(encoded_features, columns=onehot_encoder.get_feature_names_out(self.cat_features))
        self.df = pd.concat([self.df.drop(columns=self.cat_features), encoded_df], axis=1)
    
    def convert_bool_to_int(self):
        """Converts boolean features to integer type."""
        for col in self.df.columns:
            if self.df[col].dtype == bool:
                self.df[col] = self.df[col].astype(int)

    def save_data(self, output_path):
        """Saves the processed DataFrame to a CSV file."""
        self.df.to_csv(output_path, index=False)
    
    def process_data(self):
        self.calculate_description_length()
        self.fill_missing()
        self.drop_unnecessary_columns()
        self.encode_categorical_features()
        self.convert_bool_to_int()
    
    def save_data(self, output_path):
        """Saves the processed DataFrame to a CSV file."""
        self.df.to_csv(output_path, index=False)