import requests
from bs4 import BeautifulSoup

LIMIT = 50

# https://kr.indeed.com/취업?q=python&limit=50&start=0


def get_last_page(url):
    result = requests.get(url)

    soup = BeautifulSoup(result.text, "html.parser")
    pagination = soup.find('div', class_='pagination')
    links = pagination.find_all('a')

    pages = []
    for link in links[:-1]:
        pages.append(int(link.string))

    max_page = pages[-1]
    return max_page


def extract_job(html, url):
    title = html.find(class_="title").find('a')['title']

    company = html.find('span', class_='company')
    company_anchor = company.find('a')

    location = html.find(class_='location').string

    job_id = html['data-jk']

    # https://kr.indeed.com/%EC%B7%A8%EC%97%85?q=python&limit=50&start=0&vjk=c6bf8184940d37c3

    if company_anchor is not None:
        company = str(company_anchor.string)
    else:
        company = str(company.string)

    company = company.strip()

    return {
        'title': title,
        'company': company,
        'location': location,
        'apply_link': f'{url}&start=0&vjk={job_id}'
    }


def get_jobs(last_page, url):
    jobs = []

    for page in range(last_page):
        print(f'Scrapping Indeed page: {page}')
        result = requests.get(f'{url}&start={page*LIMIT}')
        soup = BeautifulSoup(result.text, "html.parser")
        # job card를 받아온 변수
        results = soup.find_all('div', class_="jobsearch-SerpJobCard")

        for result in results:
            job = extract_job(result, url)
            jobs.append(job)

    return jobs


def get_indeed_jobs(word):
    url = f"https://kr.indeed.com/취업?q={word}&limit={LIMIT}"
    last_page = get_last_page(url)
    jobs = get_jobs(last_page, url)

    return jobs
