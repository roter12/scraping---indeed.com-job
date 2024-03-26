import os
import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup # beautifulsoup4


# Get html content
def get_indeed_job_list_html(start = 0, query = 'python'):
    if start == 0:
        url = f'https://ca.indeed.com/jobs?q={query}'
    else:
        url = f'https://ca.indeed.com/jobs?q={query}&start={start}'
    driver = webdriver.Chrome()
    driver.get(url)
    return driver.page_source


# Parse html
def parse_indeed_job_list(html):

    # Parse html
    data = {'Title': [],
            'Company': [],
            'Location': [],
            'MetaData': [],
            'Date': [],
            'Content': [],
            'URL': []}

    soup = BeautifulSoup(html, "html.parser")
    for f in soup.findAll('li', attrs={'class':'css-5lfssm eu4oa1w0'}):
        
        el = f.find('a', class_='jcs-JobTitle css-jspxzf eu4oa1w0')
        if el is not None:
            data['Title'].append(el.span.text)
            data['URL'].append(el['href'])
            print(f"Job: {el.span.text}")
        else:
            continue

        el = f.find('span', class_='companyName')
        if el is not None:
            data['Company'].append(el.text)
        else:
            data['Company'].append('')
        
        el = f.find('div', class_='companyLocation')
        if el is not None:
            data['Location'].append(el.text)
        else:
            data['Location'].append('')

        el = f.find('div', class_='attribute_snippet')
        if el is not None:
            data['MetaData'].append(el.text)
        else:
            data['MetaData'].append('')

        el = f.find('span', class_='date')
        if el is not None:
            data['Date'].append(el.text)
        else:
            data['Date'].append('')

        el = f.find('div', class_='job-snippet')
        if el is not None:
            li = el.findAll('li')
            text = el.text
            for l in li:
                text = text + l.text + '\n'
            data['Content'].append(text)
        else:
            data['Content'].append('')

    # Save DataFrame to XLSX
    saveFile = 'indeed_jobs.xlsx'
    if os.path.exists(saveFile):
        df1 = pd.read_excel(saveFile)
        df2 = pd.DataFrame(data)
        df = pd.concat([df1, df2], ignore_index = True)
    else:
        df = pd.DataFrame(data)
    df.to_excel(saveFile, index=False)

    print(f"Added {len(data['Title'])} jobs successfully to {saveFile}!")


# Save as a file
def save_file(text, filename = 'test.tmp'):
    file = open(filename, "w", encoding="utf-8")
    file.write(text)
    file.close()


# Read file
def read_file(filename = 'test.tmp'):
    file = open(filename, "r", encoding="utf-8")
    text = file.read()
    file.close()
    return text


# Main entry
for x in range(10):
    html = get_indeed_job_list_html(x * 10)
    # save_file(html)
    parse_indeed_job_list(html)