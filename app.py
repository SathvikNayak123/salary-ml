from flask import Flask, request, render_template
from pipeline.prediction_pipeline import PredictPipeline
import pandas as pd

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data
    company_name = request.form['company_name']
    location = request.form['location']
    ownership = request.form['ownership']
    industry = request.form['industry']
    sector = request.form['sector']
    job_simp = request.form['job_simp']
    seniority = request.form['seniority']
    size_upper = request.form['size_upper']
    revenue_upper = request.form['revenue_upper']

    # Extract numeric values
    rating = float(request.form['rating'])
    age = int(request.form['age'])
    desc_len = int(request.form['desc_len'])
    
    # Extract skills knowledge
    ml_yn = int(request.form['ml_yn'])
    dl_yn = int(request.form['dl_yn'])
    ai_yn = int(request.form['ai_yn'])
    python_yn = int(request.form['python_yn'])
    sql_yn = int(request.form['sql_yn'])
    tool_yn = int(request.form['tool_yn'])
    cloud_yn = int(request.form['cloud_yn'])

    col = pd.read_csv("artifacts/data_transform.csv").columns
    
    input_dict = {
        'Rating': rating,
        'ml_yn': ml_yn,
        'dl_yn': dl_yn,
        'ai_yn': ai_yn,
        'python_yn': python_yn,
        'sql_yn': sql_yn,
        'tool_yn': tool_yn,
        'cloud_yn': cloud_yn,
        'desc_len': desc_len,
        'Age': age,
        # Company Name encodings
        'Company Name_Accusaga': 1 if company_name == 'Accusaga' else 0,
        'Company Name_Applied Materials': 1 if company_name == 'Applied Materials' else 0,
        'Company Name_Arch Systems LLC': 1 if company_name == 'Arch Systems LLC' else 0,
        'Company Name_Barclays': 1 if company_name == 'Barclays' else 0,
        'Company Name_Blackcoffer (OPC) Pvt. Ltd': 1 if company_name == 'Blackcoffer (OPC) Pvt. Ltd' else 0,
        'Company Name_Boston Consulting Group': 1 if company_name == 'Boston Consulting Group' else 0,
        'Company Name_Drimlite': 1 if company_name == 'Drimlite' else 0,
        'Company Name_Excellent Opportunity': 1 if company_name == 'Excellent Opportunity' else 0,
        'Company Name_Expedia Partner Solutions': 1 if company_name == 'Expedia Partner Solutions' else 0,
        'Company Name_Exponentia.ai': 1 if company_name == 'Exponentia.ai' else 0,
        'Company Name_IPCS Global solutions pvt ltd': 1 if company_name == 'IPCS Global solutions pvt ltd' else 0,
        'Company Name_Indicraft Vintage Private Limited': 1 if company_name == 'Indicraft Vintage Private Limited' else 0,
        'Company Name_Innovecture': 1 if company_name == 'Innovecture' else 0,
        'Company Name_Louis Dreyfus Company': 1 if company_name == 'Louis Dreyfus Company' else 0,
        'Company Name_MacroCosmos Creations': 1 if company_name == 'MacroCosmos Creations' else 0,
        'Company Name_Michelin': 1 if company_name == 'Michelin' else 0,
        'Company Name_Nithminds Private limited': 1 if company_name == 'Nithminds Private limited' else 0,
        'Company Name_S&P Global': 1 if company_name == 'S&P Global' else 0,
        'Company Name_Saaki Argus & Averil Consulting': 1 if company_name == 'Saaki Argus & Averil Consulting' else 0,
        'Company Name_WAHY LAB SOLUTIONS': 1 if company_name == 'WAHY LAB SOLUTIONS' else 0,
        'Company Name_objectways': 1 if company_name == 'objectways' else 0,

        # Location encodings
        'Location_Chennai': 1 if location == 'Chennai' else 0,
        'Location_Cochin': 1 if location == 'Cochin' else 0,
        'Location_Coimbatore': 1 if location == 'Coimbatore' else 0,
        'Location_Gurgaon': 1 if location == 'Gurgaon' else 0,
        'Location_Hyderābād': 1 if location == 'Hyderābād' else 0,
        'Location_India': 1 if location == 'India' else 0,
        'Location_Pune': 1 if location == 'Pune' else 0,
        'Location_Remote': 1 if location == 'Remote' else 0,

        # Type of ownership encodings
        'Type of ownership_Company - Public': 1 if ownership == 'Company - Public' else 0,
        'Type of ownership_Private Practice / Firm': 1 if ownership == 'Private Practice / Firm' else 0,
        'Type of ownership_Subsidiary or Business Segment': 1 if ownership == 'Subsidiary or Business Segment' else 0,
        'Type of ownership_Unknown': 1 if ownership == 'Unknown' else 0,

        # Industry encodings
        'Industry_Business consulting': 1 if industry == 'Business consulting' else 0,
        'Industry_Computer Hardware Development': 1 if industry == 'Computer Hardware Development' else 0,
        'Industry_Crop Production': 1 if industry == 'Crop Production' else 0,
        'Industry_Electronics Manufacturing': 1 if industry == 'Electronics Manufacturing' else 0,
        'Industry_HR Consulting': 1 if industry == 'HR Consulting' else 0,
        'Industry_Information Technology Support Services': 1 if industry == 'Information Technology Support Services' else 0,
        'Industry_Internet & Web Services': 1 if industry == 'Internet & Web Services' else 0,
        'Industry_Machinery Manufacturing': 1 if industry == 'Machinery Manufacturing' else 0,
        'Industry_Research and development': 1 if industry == 'Research and development' else 0,
        'Industry_unknown': 1 if industry == 'unknown' else 0,

        # Sector encodings
        'Sector_Finance': 1 if sector == 'Finance' else 0,
        'Sector_Human resources and staffing': 1 if sector == 'Human resources and staffing' else 0,
        'Sector_Information Technology': 1 if sector == 'Information Technology' else 0,
        'Sector_Management and consulting': 1 if sector == 'Management and consulting' else 0,
        'Sector_Manufacturing': 1 if sector == 'Manufacturing' else 0,
        'Sector_unknown': 1 if sector == 'unknown' else 0,

        # Job simplifications
        'job_simp_data analyst': 1 if job_simp == 'data analyst' else 0,
        'job_simp_data scientist': 1 if job_simp == 'data scientist' else 0,
        'job_simp_manager': 1 if job_simp == 'manager' else 0,

        # Seniority encodings
        'seniority_senior': 1 if seniority == 'senior' else 0,

        # Revenue encodings
        'Revenue_Upper_10 000': 1 if revenue_upper == '10 000' else 0,
        'Revenue_Upper_25': 1 if revenue_upper == '25' else 0,
        'Revenue_Upper_unknown': 1 if revenue_upper == 'unknown' else 0,

        # Size encodings
        'Size_Upper_200': 1 if size_upper == '200' else 0,
        'Size_Upper_50': 1 if size_upper == '50' else 0,
        'Size_Upper_500': 1 if size_upper == '500' else 0,
        'Size_Upper_Unknown': 1 if size_upper == 'Unknown' else 0,
    }

    # Convert to DataFrame
    input_data = pd.DataFrame([input_dict], columns=col).to_numpy().reshape(1, -1)

    obj=PredictPipeline()

    prediction = obj.give_prediction(input_data)
    
    return render_template('index.html', prediction_text=f'Predicted Salary: ${prediction[0]:.2f}')

if __name__ == '__main__':
    app.run(debug=True)
