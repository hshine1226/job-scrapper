import requests
from bs4 import BeautifulSoup

# https://stackoverflow.com/jobs?q=python
# https://stackoverflow.com/jobs?q=python&pg=2
URL = f"https://stackoverflow.com/jobs?q=python"


def get_last_page(url):
    result = requests.get(url)

    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find('div', class_='s-pagination')
    if not pagination:
        return 1

    links = pagination.find_all('a', class_='s-pagination--item')
    span = []
    for link in links:
        span.append(link.find('span').string)
    pages = span[:-2]
    max_page = int(pages[-1])
    return max_page


def extract_job(html):
    title = html.find('a', class_='s-link')['title']
    company, location = html.find('h3').find_all('span')

    company = company.get_text(strip=True)
    location = location.get_text(strip=True)
    job_id = int(html['data-jobid'])

    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f'https://stackoverflow.com/jobs/{job_id}'
    }


def get_jobs(last_page, url):
    jobs = []

    for page in range(last_page):
        print(f"Scrapping Stack Overflow Page: {page}")
        result = requests.get(f'{url}&pg={page+1}')
        soup = BeautifulSoup(result.text, "html.parser")
        # # job card를 받아온 변수
        results = soup.find_all('div', class_='-job')
        for result in results:
            job = extract_job(result)
            jobs.append(job)
    return jobs


def get_so_jobs(word):
    url = f"https://stackoverflow.com/jobs?q={word}"
    last_page = get_last_page(url)
    jobs = get_jobs(last_page, url)

    return jobs
