# indeed_scrape.py - scrape major tech job listings from indeed_
import re
from urllib import parse
from ast import literal_eval
from pdb import set_trace as bp

import requests
from bs4 import BeautifulSoup


def build_url(site, *args, job=None, state=None, page=0, join_next=False):
    """
    Build url for specific sites

    join_next: if True, join base with tail from next page
    """
    if site == "indeed":
        job_query = "jobs?q="
        loc_query = "&l="
        page_query = "&start="

        base = "https://www.indeed.com"

        if join_next:
            tail = args[0][1:]
            url = parse.urljoin(base, tail)
            return url

        job = job_query + parse.quote(job)
        loc = loc_query + parse.quote(state)
        page = page_query + str(page)

        tail = job + loc + page
        url = parse.urljoin(base, tail)

        return url


def fetch_page_listings(job, state, site, page=0):
    """
    Gets all job listings in one state for one title,
    returns a list of jobs to be written to csv

    job: name of job in string form

    state: state name in string form

    site: site name in string form
    """
    initial_url = build_url(site, job=job, state=state, page=page)
    ua = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) "
          "Gecko/20100101 Firefox/78.0")
    HEADERS = {"User-Agent": ua}

    res = requests.get(initial_url, headers=HEADERS)
    try:
        res.raise_for_status()
    except Exception as err:
        print(err)

    soup = BeautifulSoup(res.text, features="html.parser")
    bp()
    try:
        next_button = soup.find_all(attrs={"aria-label": "Next"})[0]
        next_page = next_button.get("href")
    except IndexError:
        next_page = None

    scripts = soup.select("script")
    jobs = scripts[25].get_text()

    ptn = re.compile(r"(jobmap\[\d+\]\=\s)(\{.*\;)")
    quote_key = re.compile(r"((\,|\{)(\w+)\:)")
    objects = re.findall(ptn, jobs)
    jobs = [v for k, v in objects]
    quoted = list(
               map(lambda x: re.sub(quote_key, "\g<2> \"\g<3>\":", x), jobs)
             )
    data = list(map(lambda x: literal_eval(x.strip(";")), quoted))

    return data, next_page


def get_all_state(job, state):
    """For one job title, get all listings in state"""
    # while aria-label='Next' get next page
    pass


def get_all_jobs(job):
    """For one job title, get all listings across US"""
    pass

# TODO: Because job counts appear to be unreliable
#       get page number. When page number is <= last
#       page number, stop getting next page

# parse javascript ***********

# TODO: use regular expression to get page number for iterations

# TODO: get details from job Card
# TODO: store details to csv


if __name__ == "__main__":
    details, next_page = fetch_page_listings("data scientist",
                                             "Texas", "indeed", page=710)
    print(details)
    print(next_page)
