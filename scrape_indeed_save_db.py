import sqlite3
import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import datetime
#create database called 'indeed.db'
db = sqlite3.connect('indeed.db')
#create cursor used to create, modify and delete table
cursor = db.cursor()
#create table
try:
    cursor.execute('''CREATE TABLE dataScientistJobs(date_scrape Date, job_link TEXT,
    job_title TEXT,job_company TEXT,job_location TEXT,job_snippet TEXT,job_date_post TEXT
    )''') 
except Exception as e:
    print('exception while creating table: ',e)

def extract(page_number):
    global url
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    url = f'https://fr.indeed.com/jobs?q=Data%20Scientist%20Junior&l=Paris%20(75)&jt=permanent&start={page_number}'
    r = requests.get(url=url, headers=headers)
    #return r.status_code
    print(r.status_code)
    soup = BeautifulSoup(r.content,"html.parser")
    return soup 

def place_holder(values):
    return '({})'.format(', '.join('?' * len(values)))

def save_row_db(values):
    cursor.execute('''INSERT INTO dataScientistJobs VALUES{}'''.format(place_holder(values)), values)
    pass

def transform(soup):
    a = soup.find_all('a',id = re.compile('^job_'))
    for each_a in a:
        base_link = os.path.dirname(url)
        job_link = base_link + each_a['href']
        div_title = each_a.find('div', class_="heading4 color-text-primary singleLineTitle tapItem-gutter")
        job_title = div_title.find('span', attrs = {'title':True}).text
        div_location = each_a.find('div', class_="heading6 company_location tapItem-gutter")
        job_company = div_location.find('span', class_="companyName").text
        job_location = div_location.find('div', class_="companyLocation").text
        job_snippet = each_a.find('div', class_="job-snippet").text
        try:
            job_date_post = each_a.find('span',class_='date').text.split('Postedil y a')[1]
        except:
            job_date_post = each_a.find('span',class_='date').text

        date_scrape = datetime.datetime.now()
        # save row to db
        values = (date_scrape,job_link,job_title,job_company,job_location,job_snippet,job_date_post)
        save_row_db(values)
   
    pass
    
url =''
dict_jobs = []
for i in range(0,20,10):
    print(f'Getting page : {i}')
    soup = extract(i)
    transform(soup)
db.commit()
#read table
# cursor.execute('''SELECT * FROM dataScientistJobs''')
# results = cursor.fetchall()
#or using pandas
results = pd.read_sql_query("SELECT * FROM dataScientistJobs",db)
print(results)
db.close()

