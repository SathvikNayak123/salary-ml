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

    # Extract numeric values
    rating = float(request.form['rating'])
    size_upper = int(request.form['size_upper'])
    age = int(request.form['age'])
    revenue_upper = int(request.form['revenue_upper'])
    desc_len = int(request.form['desc_len'])
    
    # Extract skills knowledge
    ml_yn = int(request.form['ml_yn'])
    dl_yn = int(request.form['dl_yn'])
    ai_yn = int(request.form['ai_yn'])
    python_yn = int(request.form['python_yn'])
    sql_yn = int(request.form['sql_yn'])
    tool_yn = int(request.form['tool_yn'])
    cloud_yn = int(request.form['cloud_yn'])
    
    input_data = pd.Series({
        'Rating': [rating],
        'ml_yn': [ml_yn],
        'dl_yn': [dl_yn],
        'ai_yn': [ai_yn],
        'python_yn': [python_yn],
        'sql_yn': [sql_yn],
        'tool_yn': [tool_yn],
        'cloud_yn': [cloud_yn],
        'Size_Upper': [size_upper],
        'Age': [age],
        'Revenue_Upper': [revenue_upper],
        'desc_len': [desc_len],
        'Company Name': [company_name],
        'Location': [location],
        'Type of ownership': [ownership],
        'Industry': [industry],
        'Sector': [sector],
        'job_simp': [job_simp],
        'seniority': [seniority]
    })

    obj=PredictPipeline()

    prediction = obj.give_prediction(input_data)
    
    return render_template('index.html', prediction_text=f'Predicted Salary: ${prediction[0]:.2f}')

if __name__ == '__main__':
    app.run(debug=True)
