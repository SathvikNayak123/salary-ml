from selenium.common.exceptions import NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException, TimeoutException
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
import time
import pandas as pd

def get_jobs(keyword, num_jobs, verbose, path, sleep_time):
    
    '''Gathers jobs as a dataframe, scraped from Glassdoor'''
    
    # Initializing the webdriver
    service = Service(executable_path=path)
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=service, options=options)
    driver.set_window_size(1120, 1000)

    url = "https://www.glassdoor.com/Job/jobs.htm?suggestCount=0&suggestChosen=false&clickSource=searchBtn&typedKeyword=" + keyword + "&sc.keyword=" + keyword + "&locT=&locId=&jobType="
    driver.get(url)
    jobs = []

    while len(jobs) < num_jobs:  # If true, should be still looking for new jobs.

        # Let the page load. Change this number based on your internet speed.
        time.sleep(sleep_time)

        # Going through each job on this page
        job_buttons = driver.find_elements(By.CLASS_NAME, "JobsList_jobListItem__wjTHv")  # These are the buttons we're going to click.
        for job_button in job_buttons:

            print("Progress: {}".format("" + str(len(jobs)) + "/" + str(num_jobs)))
            if len(jobs) >= num_jobs:
                break
            
            # Handle the "Sign Up" if it appears
            try:
                close_button = driver.find_element(By.XPATH, '//button[contains(@class, "CloseButton")]')
                close_button.click()
                print('Close button clicked successfully')
            except NoSuchElementException:
                pass
            except ElementClickInterceptedException:
                print('Click intercepted while trying to close the modal')
            
            try:
                job_button.click()
                time.sleep(1)  # Wait a bit to allow the job details to load
                
                # Handle the "Sign Up" if it appears
                try:
                    close_button = driver.find_element(By.XPATH, '//button[contains(@class, "CloseButton")]')
                    close_button.click()
                    print('Close button clicked successfully')
                except NoSuchElementException:
                    pass
                except ElementClickInterceptedException:
                    print('Click intercepted while trying to close the modal')

                # Collect job details with a timeout
                collected_successfully = False
                start_time = time.time()
                while not collected_successfully and (time.time() - start_time) < sleep_time:
                    try:
                        #driver.set_page_load_timeout(10)
                        company_name = driver.find_element(By.XPATH, './/h4[contains(@class, "heading_Heading__BqX5J")]').text
                        location = driver.find_element(By.XPATH, './/div[@class="JobDetails_location__mSg5h"]').text
                        job_title = driver.find_element(By.XPATH, './/h1[contains(@class, "heading_Heading__BqX5J")]').text
                        job_description = driver.find_element(By.XPATH, './/div[contains(@class, "JobDetails_jobDescription__uW_fK")]').text
                        collected_successfully = True
                    except (NoSuchElementException, TimeoutException):
                        time.sleep(sleep_time) 

                if not collected_successfully:
                    print('Skipping job due to load timeout.')
                    continue  # Skip this job and move to the next
                
                try:
                    salary_estimate = driver.find_element(By.XPATH, './/div[@class="SalaryEstimate_medianEstimate__fOYN1"]').text
                except NoSuchElementException:
                    salary_estimate = None

                try:
                    rating = driver.find_element(By.XPATH, './/div[@id="rating-headline"]').text
                except NoSuchElementException:
                    rating = None

                # Printing for debugging
                if verbose:
                    print("Job Title: {}".format(job_title))
                    print("Salary Estimate: {}".format(salary_estimate))
                    print("Job Description: {}".format(job_description[:500]))
                    print("Rating: {}".format(rating))
                    print("Company Name: {}".format(company_name))
                    print("Location: {}".format(location))

                # Going to the Company tab...
                try:
                    size = driver.find_element(By.XPATH, './/span[text()="Size"]/following-sibling::div').text
                except NoSuchElementException:
                    size = None

                try:
                    founded = driver.find_element(By.XPATH, './/span[text()="Founded"]/following-sibling::div').text
                except NoSuchElementException:
                    founded = None

                try:
                    type_of_ownership = driver.find_element(By.XPATH, './/span[text()="Type"]/following-sibling::div').text
                except NoSuchElementException:
                    type_of_ownership = None

                try:
                    industry = driver.find_element(By.XPATH, './/span[text()="Industry"]/following-sibling::div').text
                except NoSuchElementException:
                    industry = None

                try:
                    sector = driver.find_element(By.XPATH, './/span[text()="Sector"]/following-sibling::div').text
                except NoSuchElementException:
                    sector = None

                try:
                    revenue = driver.find_element(By.XPATH, './/span[text()="Revenue"]/following-sibling::div').text
                except NoSuchElementException:
                    revenue = None

                if verbose:
                    print("Size: {}".format(size))
                    print("Founded: {}".format(founded))
                    print("Type of Ownership: {}".format(type_of_ownership))
                    print("Industry: {}".format(industry))
                    print("Sector: {}".format(sector))
                    print("Revenue: {}".format(revenue))
                    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

                jobs.append({"Job Title": job_title,
                             "Salary Estimate": salary_estimate,
                             "Job Description": job_description,
                             "Rating": rating,
                             "Company Name": company_name,
                             "Location": location,
                             "Size": size,
                             "Founded": founded,
                             "Type of ownership": type_of_ownership,
                             "Industry": industry,
                             "Sector": sector,
                             "Revenue": revenue,
                            })

            except (NoSuchElementException, ElementClickInterceptedException, ElementNotInteractableException) as e:
                print(f"An error occurred: {e}")
                continue  # Move to the next job button

        # Clicking on the "next page" button
        try:
            next_button = driver.find_element(By.CLASS_NAME, "button_Button__MlD2g")
            next_button.click()
        except NoSuchElementException:
            print("Scraping terminated before reaching the target number of jobs. Needed {}, got {}.".format(num_jobs, len(jobs)))
            break

    driver.quit()
    return pd.DataFrame(jobs)  # This line converts the dictionary object into a pandas DataFrame.
