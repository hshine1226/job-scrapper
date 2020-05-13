from so import get_so_jobs
from indeed import get_indeed_jobs


def get_jobs(word):
    jobs = get_so_jobs(word) + get_indeed_jobs(word)
    return jobs
