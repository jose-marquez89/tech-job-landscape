# indeed_scrape.py - scrape major tech job listings from indeed_
import re
from urllib import parse

import requests
from bs4 import BeautifulSoup



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

    # TODO: add elif for other sites


def fetch_listings(job, state, base_url):
    """get all job listings in one state for one title"""
    initial_url = build_url(base_url, job, state, 0)

    res = requests.get(initial_url)
    try:
        res.raise_for_status()
    except Exception as err:
        print(err)

    soup = BeautifulSoup(res.text)
    # TODO: Because job counts appear to be unreliable
    #       get page number. When page number is <= last
    #       page number, stop getting next page

    # parse javascript ***********

    # TODO: use regular expression to get page number for iterations

    # TODO: get details from job Card
    # TODO: store details to csv
    pass


if __name__ == "__main__":
    indeed = "https://www.indeed.com"
    print(build_url(indeed, "data analyst", "new hampshire", 20))
