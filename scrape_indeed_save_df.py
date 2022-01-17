import requests
from bs4 import BeautifulSoup
import re
import os
import pandas as pd
import datetime
def extract(page_number):
    global url
    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}
    url = f'https://fr.indeed.com/jobs?q=Data%20Scientist%20Junior&l=Paris%20(75)&jt=permanent&start={page_number}'
    r = requests.get(url=url, headers=headers)
    #return r.status_code
    print(r.status_code)
    soup = BeautifulSoup(r.content,"html.parser")
    return soup 
def transform(soup):
    # div = soup.find_all('div', id="mosaic-provider-jobcards")
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
        # job_description        
        job = {'job_link':job_link,
        'job_title':job_title,
         'job_company':job_company,
         'job_location':job_location,
         'job_snippet':job_snippet,
         'job_date_post':job_date_post,
         'date_scrape':date_scrape
         }
        dict_jobs.append(job)
    
    return
    
url =''
dict_jobs = []
for i in range(0,20,10):
    print(f'Getting page : {i}')
    soup = extract(i)
    transform(soup)
df = pd.DataFrame(dict_jobs)
print(df.head())
df.to_csv('jobs.csv')
