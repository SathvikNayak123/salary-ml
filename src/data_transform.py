import pandas as pd
from sklearn.preprocessing import OneHotEncoder
from sklearn.preprocessing import StandardScaler

df=pd.read_csv('artifacts/data_cleaned.csv')

# job description length
df['desc_len'] = df['Job Description'].apply(lambda x: len(x))
df['desc_len']

num_features = ['Rating','avg_salary', 'ml_yn', 'dl_yn', 'ai_yn','python_yn', 'sql_yn', 'tool_yn', 'cloud_yn', 'Size_Upper', 'Age','Revenue_Upper', 'desc_len']
cat_features = ['Company Name', 'Location', 'Type of ownership', 'Industry', 'Sector', 'job_simp', 'seniority']

# convert dtypes
for col in num_features:
    df[col] = pd.to_numeric(df[col], errors='coerce')

for col in cat_features:
    df[col] = df[col].astype('category')

# Fill missing values in numeric columns with the mean
for col in num_features:
    df[col].fillna(df[col].mean(), inplace=True)

# Fill missing values in categorical columns with the mode
for col in cat_features:
    df[col].fillna(df[col].mode()[0], inplace=True)

df=df.drop(['Job Title', 'Salary Estimate', 'Job Description'],axis=1)

# Initialize OneHotEncoder
onehot_encoder = OneHotEncoder(sparse=False, drop='first')
# Fit and transform the categorical features
encoded_features = onehot_encoder.fit_transform(df[cat_features])
# Create a DataFrame with the encoded features
encoded_df = pd.DataFrame(encoded_features, columns=onehot_encoder.get_feature_names_out(cat_features))
# Concatenate with the original DataFrame
df = pd.concat([df.drop(columns=cat_features), encoded_df], axis=1)

# Initialize the StandardScaler
scaler = StandardScaler()
# Fit and transform the numeric features
df[['Rating','Size_Upper', 'Age', 'desc_len']] = scaler.fit_transform(df[['Rating','Size_Upper', 'Age', 'desc_len']])

df.to_csv('artifacts/data_transformed.csv')