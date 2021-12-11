import logging
from worker_pool.services import crawler
from worker_pool.adapters.broker import Broker, RedisBroker
from worker_pool.domain.tasks import DownloadWebsite
from worker_pool.exceptions.pool_exceptions import CrawlingException
import os
from worker_pool import config
import time

logging.basicConfig(**config.get_logger_config("master_logs.txt"))
logger = logging.getLogger(__name__)


def master(broker: Broker):
    """
    The master function which crawl the website and put the links into the redis queue

    :param RedisBroker: the broker which can enqueue and get tasks from the queue
    :return None
    """
    try:
        logger.info("getting the countries name")
        countries = crawler.get_countries()
    except CrawlingException as e:
        return logger.error(f"crawling exception durring country fetching: {str(e)}")

    for country_link, country_name in countries:
        try:
            for webs_link, webs_name in crawler.get_websites(country_link):
                broker.enqueue(
                    DownloadWebsite(
                        link=webs_link,
                        save_path=os.path.join(
                            config.ROOT_DIRECTORY, country_name, webs_name + ".html"
                        ),
                    )
                )
        except CrawlingException as e:
            logging.warning(f"crawling exception durring websites fetching: {str(e)}")


def main():
    broker = RedisBroker()

    master(broker)

    # run forever if it's configured
    while config.RUN_FOREVER:
        time.sleep(config.WAIT_TIME)
        master(broker)


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        logger.info("gracefully shutting down")
    except Exception as e:
        logger.error(f"unexpected error: {str(e)}")
