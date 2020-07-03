# get_headings.py - get the list of 41 jobs at
# https://skillcrush.com/blog/41-tech-job-titles/
import re
import requests
from bs4 import BeautifulSoup as bs

res = requests.get("https://skillcrush.com/blog/41-tech-job-titles/")
try:
    res.raise_for_status()
except Exception as err:
    print(err)

target = re.compile(r"\d+\.\s")

job_list = bs(res.text)

jobs = job_list.select("h3 > strong")

if __name__ == "__main__":

    with open("job_list.txt", "w") as jobfile:
        for job in jobs:
            jobfile.write(re.sub(target, "", job.text) + "\n")
