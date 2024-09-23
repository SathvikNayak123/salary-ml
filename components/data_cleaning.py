import pandas as pd
import os

class JobDataClean:
    def __init__(self):
        self.df = pd.read_csv("artifacts/glassdoor_jobs.csv")

    def title_simplifier(self, title):
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

    def seniority(self, title):
        if 'sr' in title.lower() or 'senior' in title.lower() or 'lead' in title.lower() or 'principal' in title.lower():
            return 'senior'
        elif 'jr' in title.lower() or 'jr.' in title.lower():
            return 'junior'
        else:
            return 'Unknown'

    def parse_job_title(self):
        self.df['job_simp'] = self.df['Job Title'].apply(self.title_simplifier)
        self.df['seniority'] = self.df['Job Title'].apply(self.seniority)

    def clean_salary(self):
        self.df = self.df.dropna(subset=['Salary Estimate'])
        self.df['Salary Estimate'] = self.df['Salary Estimate'].str.replace('₹', '') \
            .str.replace('L', '*100000').str.replace('T', '*1000') \
            .str.replace(r'\(Glassdoor est.\)', '', regex=True) \
            .str.replace(r'\(Employer est.\)', '', regex=True) \
            .str.replace(r'/yr', '', regex=True) \
            .str.replace(r'/mo', '*12', regex=True) \
            .str.replace(r'/hr', '*2080', regex=True)
        self.df['avg_salary'] = self.df['Salary Estimate'].apply(
            lambda x: (eval(x.split('–')[0].strip()) + eval(x.split('–')[1].strip()))/2 if '–' in str(x) else eval(x))

    def clean_size(self):
        self.df['Size_Upper'] = self.df['Size'].str.replace('10000+ Employees', 'large') \
                            .str.replace('201 to 500 Employees', 'high') \
                            .str.replace('51 to 200 Employees', 'med') \
                            .str.replace('1 to 50 Employees', 'low') \
                            .str.strip()

    def clean_founded(self):
        self.df['Founded'] = pd.to_numeric(self.df['Founded'], errors='coerce')
        self.df['Age'] = 2024 - self.df['Founded'].dropna().astype(int)

    def clean_industry_sector_ownership(self):
        self.df['Industry'] = self.df['Industry'].apply(lambda x: 'unknown' if x == '--' else x)
        self.df['Sector'] = self.df['Sector'].apply(lambda x: 'unknown' if x == '--' else x)
        self.df['Ownership'] = self.df['Type of ownership'].str.replace('Company - Private', 'private') \
                                .str.replace('Company - Public', 'publlic') \
                                .str.replace('Subsidiary or Business Segment', 'subsidiary') \
                                .str.replace('Private Practice / Firm', 'firm') \
                                .str.strip()

    def clean_revenue(self):
        self.df['Revenue_Upper'] = self.df['Revenue'].str.replace(r'\$5 to \$10 billion \(USD\)', 'med', regex=True) \
                                    .str.replace(r'\$10\+ billion \(USD\)', 'high', regex=True) \
                                    .str.replace(r'\$5 to \$25 million \(USD\)', 'low', regex=True) \
                                    .str.replace(r'Unknown / Non-Applicable', 'Unknown', regex=True) \
                                    .str.strip()

    def drop_unused_columns(self):
        self.df = self.df.drop(['Job Title', 'Salary Estimate', 'Job Description', 'Size', 'Founded', 'Revenue','Type of ownership'], axis=1)

    def save_cleaned_data(self):
        directory = os.path.dirname("artifacts/data_clean.csv")
        if not os.path.exists(directory):
            os.makedirs(directory)
        self.df.to_csv("artifacts/data_clean.csv", index=False)

    def clean_data(self):
        self.parse_job_title()
        self.clean_salary()
        self.df[['Type of ownership', 'Industry', 'Sector','Revenue','Size']] = self.df[['Type of ownership', 'Industry', 'Sector','Revenue', 'Size']].fillna('Unknown')
        self.clean_size()
        self.clean_founded()
        self.clean_industry_sector_ownership()
        self.clean_revenue()
        self.drop_unused_columns()
        self.save_cleaned_data()

if __name__=="__main__":
    job_data_cleaner = JobDataClean()
    job_data_cleaner.clean_data()



