import pandas as pd

df=pd.read_csv('artifacts/glassdoor_jobs.csv')

#parsing 'Salary'
df['Salary Estimate'] = df['Salary Estimate'].str.replace('₹', ' ')
df['Salary Estimate'] = df['Salary Estimate'].str.replace('L', ' ')

#parsing 'Job Description'
skills = {
    'Machine Learning': 'ml_yn',
    'Deep Learning': 'dl_yn',
    ('Generative AI', 'Gen AI'): 'ai_yn',
    'python': 'python_yn',
    'database': 'sql_yn',
    ('tensorflow', 'pytorch'): 'tool_yn',
    'cloud': 'cloud_yn'
}

# Loop through the skills dictionary to create and populate the columns
for skill, column in skills.items():
    if isinstance(skill, tuple):  # Check if the skill is a tuple (list of skills)
        df[column] = df['Job Description'].apply(lambda x: any(kw in x.lower() for kw in skill)).astype(int)
    else:
        df[column] = df['Job Description'].str.contains(skill, case=False, na=False).astype(int)

print(df)


# parsing 'Size'
df['Size']=df['Size'].str.replace('Employees',' ')
df['Size']=df['Size'].str.replace('+',' ')
df['Size']=df['Size'].str.replace('to','-')
# Extract the upper limit of the size range
df['Size_Upper'] = df['Size'].apply(lambda x: x.split('-')[1].strip() if '-' in str(x) else x)

# Convert the 'Founded' column to numeric, forcing errors(i.e '--' values) to NaN
df['Founded'] = pd.to_numeric(df['Founded'], errors='coerce')
df['Age'] = 2024 - df['Founded'].dropna().astype(int) # considering nan values

df['Industry'] = df['Industry'].apply(lambda x: 'unknown' if x == '--' else x)

df['Sector'] = df['Sector'].apply(lambda x: 'unknown' if x == '--' else x)

# parsing 'Revenue'
df['Revenue']=df['Revenue'].str.strip()
df['Revenue']=df['Revenue'].str.replace('billion',',000')
df['Revenue']=df['Revenue'].str.replace('million',' ')
df['Revenue']=df['Revenue'].str.replace('$',' ')
df['Revenue']=df['Revenue'].str.replace('to','-')
df['Revenue']=df['Revenue'].str.replace('Unknown / Non-Applicable','unknown')
df['Revenue']=df['Revenue'].str.replace('USD',' ')
df['Revenue']=df['Revenue'].str.replace('(',' ')
df['Revenue']=df['Revenue'].str.replace(')',' ')
#Extract upper limit of revenue
df['Revenue_Upper'] = df['Revenue'].apply(lambda x: x.split('-')[1].strip() if '-' in str(x) else x)

df = df.drop(['Size', 'Founded', 'Revenue'], axis=1)

df.to_csv('artifacts/data_cleaned.csv', index=False)