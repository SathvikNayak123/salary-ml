from glassdoor_scraper import get_jobs
import pandas as pd 

path = "chromedriver.exe"

df = get_jobs('data scientist',1000, False, path, 5)

df.to_csv('artifacts/glassdoor_jobs.csv', index = False)