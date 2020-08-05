# indeed_scrape.py - scrape major tech job listings from indeed
import re
import os
import csv
from urllib import parse
from ast import literal_eval
from pprint import pprint
from pdb import set_trace as bp
import logging

import requests
from bs4 import BeautifulSoup

FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
logging.basicConfig(level=logging.DEBUG, format=FORMAT)


def build_url(site, *args, job=None, state=None, join_next=False):
    """
    Build url for specific sites

    join_next: if True, join base with tail from next page
    """
    if site == "indeed":
        job_query = "jobs?q="
        loc_query = "&l="
        page_query = "&start=0"

        base = "https://www.indeed.com"

        if join_next:
            tail = args[0][1:]
            url = parse.urljoin(base, tail)
            return url

        job = job_query + parse.quote(job)
        loc = loc_query + parse.quote(state)

        tail = job + loc + page_query
        url = parse.urljoin(base, tail)

        return url


def fetch_with_js(job, state, site, page=0):
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


def fetch_page_listings(site, job_name=None, state=None, next_page=None):
    """
    Gets all job listings in one state for one title,
    returns a list of jobs to be written to csv

    job_name: name of job in string form

    state: state name in string form

    site: site name in string form

    next_page: the following page link, if exists
    """
    if next_page:
        initial_url = build_url(site, next_page,
                                join_next=True)
    else:
        initial_url = build_url(site, job=job_name, state=state)
    ua = ("Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:78.0) "
          "Gecko/20100101 Firefox/78.0")
    HEADERS = {"User-Agent": ua}

    res = requests.get(initial_url, headers=HEADERS)
    try:
        res.raise_for_status()
    except Exception as err:
        print(err)

    soup = BeautifulSoup(res.text, features="html.parser")
    try:
        next_button = soup.find_all(attrs={"aria-label": "Next"})[0]
        next_page = next_button.get("href")
    except IndexError:
        next_page = None

    data = []
    cards = soup.find_all("div", class_="jobsearch-SerpJobCard")
    for job in cards:
        job_data = {"search_field": job, "role": "", "company": "",
                    "location": "", "pay": "", "remote": 0,
                    "details": "", "job_post_age": ""}

        job_data["role"] = job.select("h2 > a")[0].get("title")

        company = job.find_all("a", attrs={"data-tn-element": "companyName"})
        if len(company) == 0:
            company = job.find_all(class_="company")
        job_data["company"] = company[0].get_text()

        location = job.find_all(class_="location"
                                       " accessible-contrast-color-location")
        job_data["location"] = location[0].get_text()

        remote = job.find_all(class_="remote")
        if len(remote) > 0:
            job_data["remote"] = 1

        summary = job.find_all(class_="summary")
        if len(summary) > 0:
            job_data["details"] = summary[0].get_text()

        pay = job.find_all(class_="salaryText")
        if len(pay) > 0:
            job_data["pay"] = pay[0].get_text()

        date = job.find_all(class_="date")
        job_data["job_post_age"] = date[0].get_text()

        data.append(job_data)

    return data, next_page


def get_all_state(site, job, state):
    """For one job title, get all listings in state"""
    details, next_page = fetch_page_listings(site, job=job, state=state)

    while next_page:
        data, next_page = fetch_page_listings(site, job=job,
                                              state=state, next_page=next_page)
        details.extend(data)

    return details


def get_all_jobs(site, job):
    """For one job title, get all listings across US"""
    data = []
    with open("state_names.txt", "r") as states:
        state_list = states.read()
        state_list = state_list.split('\n')

    # remove the trailing newline character
    state_list.pop()

    for state in state_list:
        state_job_data = get_all_state(site, job, state)
        data.extend(state_job_data)

    return data


def build_dataset(site):
    """Builds entire tech dataset"""
    filename = f"{site}_jobs.csv"
    with open("job_list.txt", "r") as jobs:
        job_list = jobs.read()
        job_list = job_list.split('\n')

    header = ["search_field", "role", "company", "location",
              "pay", "remote", "details", "job_post_age"]

    if os.path.isfile(filename):
        with open(filename, "w") as f:
            writer = csv.writer(f, delimiter='\t')
            writer.writerow(header)

    # remove trailing newline
    job_list.pop()
    # extract data and create rows
    for job in job_list:
        data = get_all_jobs(site, job)
        writable = []
        # may be able to speed this up by not using a dictionary
        # slowing this process down may not be entirely undesirable
        for element in data:
            writable.append(element.values())
            with open(filename, "a") as jobs_csv:
                writer = csv.writer(jobs_csv, delimiter='|')
                for row in writable:
                    writer.writerow(row)
    """
    job_data = {"role": "", "company": "", "location": "", "pay": "",
                "remote": 0, "details": "", "job_post_age": ""}
    """


if __name__ == "__main__":
    build_dataset("indeed")
