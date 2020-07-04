# indeed_scrape.py - scrape major tech job listings from indeed_
import requests
from urllib import parse

base_url = "https://www.indeed.com"
job_query = "jobs?q="
loc_query = "&l="
page_query = "&start="


def build_url(site, job, state, page):
    """build url for specific sites"""
    if site == "https://www.indeed.com":
        job_query = "jobs?q="
        loc_query = "&l="
        page_query = "&start="

        base = "https://www.indeed.com"
        job = job_query + parse.quote(job)
        loc = loc_query + parse.quote(state)
        page = page_query + str(page)

        tail = job + loc + page

        url = parse.urljoin(base, tail)

        return url


def fetch_listings(job, state, base, ):
    """get all job listings in one state for one title"""


if __name__ == "__main__":
    indeed = "https://www.indeed.com"
    print(build_url(indeed, "data analyst", "new hampshire", 20))
