from flask import Flask, request, render_template
from pipeline.prediction_pipeline import PredictPipeline
import pandas as pd
import numpy as np

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    # Extract form data

    #Extract categorical values
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

    input_dict = {
        'Rating': rating,
        'Company Name': company_name,
        'Location': location,
        'Ownership': ownership,
        'Industry': industry,
        'Sector': sector,
        'job_simp': job_simp,
        'seniority': seniority,
        'Revenue_Upper':revenue_upper,
        'Size_Upper':size_upper,
        'Age':age
    }
    
    input_data = pd.DataFrame([input_dict])

    obj=PredictPipeline()

    prediction = obj.give_prediction(input_data)
    
    prediction2 = np.exp(prediction[0])
    return render_template('index.html', prediction_text=f'Predicted Salary: Rs.{prediction2:.2f} p.a')

if __name__ == '__main__':
    app.run(debug=True)
