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
    # parse js on page to get main job details
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

    # TODO: get age of job listings
    #       this may require building
    #       the data from html if indices
    #       do not match
    #       At the moment, they DO seem
    #       to match. the tag is <span class="date ">30+ days ago</span>
    #       However, upon further inspection of the page, being able to
    #       identify if a job is remote could be an important detail

    return data, next_page


def get_all_state(job, state):
    """For one job title, get all listings in state"""
    # details, next_page = fetch_page_listings()
    # while next_page:
    #    keep getting details
    #    url = build_url("indeed", next_page)
    #    more_details, next_page = fetch_page_listings()
    #    details.update(more_details)
    # return dictionary
    pass


def get_all_jobs(job):
    """For one job title, get all listings across US"""
    # states = a list of states
    # data = {}
    # for state in states:
    #     state = get_all_state()
    #     data.update(state)
    # return data
    pass


def build_dataset(data):
    # extract data and create rows
    # write rows to csv
    pass


if __name__ == "__main__":
    details, next_page = fetch_page_listings("data scientist",
                                             "Texas", "indeed", page=710)
    print(details)
    print(next_page)
