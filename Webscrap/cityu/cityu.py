import json
import time

import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from webdriver_manager.chrome import ChromeDriverManager

# Setup Chrome options
chrome_options = webdriver.ChromeOptions()

# Initialize WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()),
                          options=chrome_options)

# Navigate to the page
entry = ("https://www.cityu.edu.hk/catalogue/ug/current/catalogue/"
         "catalogue_UC.htm?page=B/B_course_index.htm")
driver.get(entry)

# Wait for the dynamic content to load
time.sleep(5)  # Adjust this delay as needed

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)\
                   AppleWebKit/537.36 (KHTML, like Gecko)\
                   Chrome/58.0.3029.110 Safari/537.3'
}

all_course_info = []

links = driver.find_elements(By.CSS_SELECTOR, "a[href*='B_course_']")
for link in links:
    href = link.get_attribute('href')
    if not href.endswith('B_course_index.htm') and\
       not href.endswith('B_course_VM.htm'):

        ref_start = href.find('B_course_') + len('B_course_')
        ref_end = href.find('.htm', ref_start)
        ref = href[ref_start:ref_end]

        course_list_url = ("https://www.cityu.edu.hk/catalogue/ug/current/"
                           f"catalogue/B/B_course_{ref}.htm")
        response = requests.get(course_list_url, headers=headers)
        soup = BeautifulSoup(response.content, 'html.parser')

        courses = soup.find_all('a', href=True)

        for course in courses:
            course_code = course.text.split(" ")[0]

            course_url = ("https://www.cityu.edu.hk/catalogue/ug/current/course/"
                          f"{course_code}.htm")
            response = requests.get(course_url, headers=headers)
            soup = BeautifulSoup(response.content, 'html.parser')

            course_info = soup.find('div', class_="formTitle").text.strip()
            course_code, course_name = course_info.split(' - ', 1)

            div_course_aims = soup.find('div', id='div_course_aims')
            course_aim = (div_course_aims.text.strip()
                          if div_course_aims
                          else '')

            # Create a dictionary with the extracted information
            course_info_dict = {
                "courseCode": course_code,
                "courseName": course_name,
                "courseDescription": course_aim
            }
            all_course_info.append(course_info_dict)

with open('cityu.json', 'w') as json_file:
    json.dump(all_course_info, json_file, indent=4)

# Close the browser
driver.quit()
