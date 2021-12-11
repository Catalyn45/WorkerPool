import logging
import requests
from urllib import parse
import re

from worker_pool.exceptions.pool_exceptions import CrawlingException, CrawlerTimedOut
from worker_pool import config
import time

logger = logging.getLogger(__name__)


def generic_get(url: str):
    """
    a generic GET request to an url

    :param url str: the url
    :return response str: the response of the request
    """

    logger.debug(f"sending GET request to url: {url}")
    try:
        time.sleep(0.5)  # sleep 0.5 seconds to void spamming (kinda)
        response = requests.get(
            url=url,
            headers={
                "User-Agent": (
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"  # modifying User-Agent like the one from browsers
                    "AppleWebKit/537.36 (KHTML, like Gecko)"
                    "Chrome/70.0.3538.77 Safari/537.36"
                )
            },
            timeout=config.REQUESTS_TIMEOUT,
        )
    except requests.exceptions.ReadTimeout:
        raise CrawlerTimedOut()
    except requests.exceptions.RequestException as e:
        raise CrawlingException(str(e))

    return response.content


COUNTRY_PATTERN = re.compile(r'<div class="tableContainer">.*?</div>', flags=re.DOTALL)
COUNTRIES_PATTERN = re.compile(
    r"<li>.*?<a href=\"(.*?)\">(.*?)</a>.*?</li>", flags=re.DOTALL
)
WEBSITES_PATTERN = re.compile(
    r'<div class="td DescriptionCell">.*?<p class="">.*?<a href="(.*?)">(.*?)</a>.*?</p>.*?</div>',
    flags=re.DOTALL,
)


def get_countries():
    """
    Get the list of the crawled countries

    :return countries list: the crawled countries
    """

    countries_url = parse.urljoin(config.BASE_URL, "countries")
    content = generic_get(countries_url)
    if not content:
        raise CrawlingException("Empty content")

    panel = re.search(COUNTRY_PATTERN, content.decode())
    if not panel:
        raise CrawlingException("Empty panel")

    panel = panel.group(0)

    countries = [
        (parse.urljoin(config.BASE_URL, link), name)
        for link, name in re.findall(COUNTRIES_PATTERN, panel)
    ]
    if not countries:
        raise CrawlingException("Empty country list")

    return countries


def get_websites(country_url: str):
    """
    get the list of the crawled websites

    :param country_url str: the country url
    :return websites list: the crawled websites
    """

    content = generic_get(country_url)
    if not content:
        raise CrawlingException("Empty content")

    websites = [
        (parse.urljoin(config.BASE_URL, link), name)
        for link, name in re.findall(WEBSITES_PATTERN, content.decode())
    ]
    if not websites:
        raise CrawlingException("Empty website list")

    return websites


def get_content(url: str):
    """
    get the content of a get request

    :param url str: the url
    :return content str: the content
    """

    content = generic_get(url)
    return content.decode()
