# parse_js.py - a simple test script to find out how to extract job data
# from each page returned from indeed 
import re
import requests
import csv

from ast import literal_eval
from bs4 import BeautifulSoup

from indeed_scrape import build_url

res = requests.get(build_url("indeed", "Data Scientist", "Texas"))
try:
    res.raise_for_status()
except Exception:
    print("Error")
soup = BeautifulSoup(res.text, features="html.parser")
scripts = soup.select("script")
jobs = scripts[25].get_text()


ptn = re.compile(r"(jobmap\[\d+]\=\s)(\{.*\;)")
quote_key = re.compile(r"((\,|\{)(\w+)\:)")
objects = re.findall(ptn, jobs)
jobs = [v for k, v in objects]
with open('jobtext.txt', 'w') as jt:
    for j in jobs:
        jt.write(j)
        jt.write('\n')

jobs = list(map(lambda x: re.sub(quote_key, "\g<2> \"\g<3>\":", x), jobs))
data = list(map(lambda x: literal_eval(x.strip(";")), jobs))


if __name__ == '__main__':
    with open("tx_fifteen.csv", "w") as tx_csv:
        writer = csv.writer(tx_csv)
        columns = ["city", "company", "country", "location", "srcname",
                   "job_title", "zip"]
        writer.writerow(columns)
        for position in data:
            details = [position["city"], position["cmp"], position["country"],
                       position["loc"], position["srcname"], position["title"],
                       position["zip"]]
            writer.writerow(details)
