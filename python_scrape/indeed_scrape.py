# indeed_scrape.py - scrape major tech job listings from indeed_
import requests
from urllib.parse import urljoin

base_url = "https://www.indeed.com"
job_query = "jobs?q="
loc_query = "&l="
page_query = "&start="
