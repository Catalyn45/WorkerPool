from datetime import time
import requests
from urllib import parse
import re

from worker_pool.exceptions.pool_exceptions import CrawlingException
from worker_pool import config

def generic_get(url):
    response = requests.get(
        url=url,
        headers={
            "User-Agent": ("Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
                           "AppleWebKit/537.36 (KHTML, like Gecko)"
                           "Chrome/70.0.3538.77 Safari/537.36"
                          )
        },
        timeout = config.REQUESTS_TIMEOUT
    )

    return response.content

def get_countries():
    countries_url = parse.urljoin(config.BASE_URL, "countries")
    content = generic_get(countries_url)
    panel = re.search(r'<div class="tableContainer">.*?</div>', content.decode(), re.DOTALL).group(0)
    countries = [(parse.urljoin(config.BASE_URL, link), name) for link, name in re.findall(r'<li>.*?<a href=\"(.*?)\">(.*?)</a>.*?</li>', panel, flags=re.DOTALL)]
    if not countries:
        raise CrawlingException("Empty country list")

    return countries


def get_websites(country_url):
    content = generic_get(country_url)
    websites = [(parse.urljoin(config.BASE_URL, link), name) for link, name in re.findall(r'<div class="td DescriptionCell">.*?<p class="">.*?<a href="(.*?)">(.*?)</a>.*?</p>.*?</div>', content.decode(), flags=re.DOTALL)]
    if not websites:
        raise CrawlingException("Empty website list")
    
    return websites
