import pandas as pd

df=pd.read_csv('artifacts/glassdoor_jobs.csv')
# parsing 'Job Title'
def title_simplifier(title):
    if 'data scientist' in title.lower():
        return 'data scientist'
    elif 'data engineer' in title.lower():
        return 'data engineer'
    elif 'analyst' in title.lower():
        return 'data analyst'
    elif 'machine learning' in title.lower():
        return 'ML engineer'
    elif 'manager' in title.lower():
        return 'manager'
    elif 'director' in title.lower():
        return 'director'
    else:
        return 'Unknown'
    
df['job_simp'] = df['Job Title'].apply(title_simplifier)
    
def seniority(title):
    if 'sr' in title.lower() or 'senior' in title.lower() or 'sr' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
    elif 'jr' in title.lower() or 'jr.' in title.lower():
        return 'junior'
    else:
        return 'Unknown'
    
df['seniority'] = df['Job Title'].apply(seniority)

# drop rows with missing salary values
df = df.dropna(subset=['Salary Estimate'])

#parsing 'Salary'
# Remove currency symbols and extraneous text
df['Salary Estimate'] = df['Salary Estimate'].str.replace('₹', '').str.replace('L', '*100000').str.replace('T', '*1000')
df['Salary Estimate'] = df['Salary Estimate'].str.replace(r'\(Glassdoor est.\)', '', regex=True)
df['Salary Estimate'] = df['Salary Estimate'].str.replace(r'\(Employer est.\)', '', regex=True)
df['Salary Estimate'] = df['Salary Estimate'].str.replace(r'/yr', '', regex=True)
df['Salary Estimate'] = df['Salary Estimate'].str.replace(r'/mo', '*12', regex=True)
df['Salary Estimate'] = df['Salary Estimate'].str.replace(r'/hr', '*2080', regex=True)  # Assuming 40 hours per week and 52 weeks per year

df['avg_salary'] = df['Salary Estimate'].apply(lambda x: eval(x.split('–')[0].strip())+eval(x.split('–')[1].strip()) if '–' in str(x) else eval(x))

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
df['Revenue'] = df['Revenue'].str.strip() \
    .str.replace(r'\$', '', regex=True) \
    .str.replace(r'to', '-', regex=False) \
    .str.replace(r'\+', '', regex=True) \
    .str.replace(r'billion', '000', regex=False) \
    .str.replace(r'million', '', regex=False) \
    .str.replace(r'Unknown / Non-Applicable', 'unknown', regex=False) \
    .str.replace(r'USD', '', regex=False) \
    .str.replace(r'\(', '', regex=True) \
    .str.replace(r'\)', '', regex=True)

#Extract upper limit of revenue
df['Revenue_Upper'] = df['Revenue'].apply(lambda x: x.split('-')[1].strip() if '-' in str(x) else x)

df = df.drop(['Size', 'Founded', 'Revenue'], axis=1)

df.to_csv('artifacts/data_cleaned.csv', index=False)