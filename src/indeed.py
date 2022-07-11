import requests
import csv
from bs4 import BeautifulSoup

LIMIT = 50

def get_last_pages(url):
    indeed_result = requests.get(url)
    indeed_soup = BeautifulSoup(indeed_result.text, 'html.parser')
    pagination = indeed_soup.find("div", {"class":"pagination"})
    links = pagination.find_all('a')
    return int(links[-2].string)

def extract_job(html):
    title = html.find("h2", {"class":"jobTitle"}).find("a").string
    company = html.find("span", {"class":"companyName"})
    company_a = company.find("a")
    if company_a is not None:
        company = str(company_a.string)
    else:
        company = str(company.string)
    company = company.strip()
    location = str(html.find("div", {"class":"companyLocation"}).text)
    job_id = html.find("h2", {"class":"jobTitle"}).find("a")["data-jk"]
    return {'title': title, 'company': company, 'location':location, 'link':f"https://www.indeed.com/viewjob?jk={job_id}"}
        

def extract_indeed_jobs(last_page, url):
    jobs = []
    for page in range(last_page):
        soup = requests.get(url)
        results = BeautifulSoup(soup.text, 'html.parser').find_all("div", {"class": "job_seen_beacon"})
        for result in results:
            job=extract_job(result)
            jobs.append(job)
    return jobs

def get_jobs(word):
    url = f"https://kr.indeed.com/%EC%B7%A8%EC%97%85?q={word}&limit={LIMIT}"
    last = get_last_pages(url)
    return extract_indeed_jobs(last, url)


def save_to_file(jobs):
    file = open("jobs.csv", mode="w")
    writer = csv.writer(file)
    writer.writerow(["title, company, location, link"])
    for job in jobs:
        writer.writerow(list(job.values()))