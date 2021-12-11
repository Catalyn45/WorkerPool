import os
import logging

REDIS_CONFIG = {"host": os.environ.get("BROKER_HOST", "localhost"), "port": 6379}
REDIS_CHANNEL_NAME = "tasks"  # queue name for the tasks

WORKERS = 4

RUN_FOREVER = False  # whether or not run the crawlers forever
WAIT_TIME = None  # number of seconds to wait until crawling again

BASE_URL = "https://www.alexa.com/topsites/"

ROOT_DIRECTORY = os.path.join(
    ".", "data", "countries"
)  # directory where all the websites will be downloaded

LOGS_DIR = os.path.join(".", "logs")  # directory for logs

REQUESTS_TIMEOUT = 2  # requests timeout in seconds


def get_logger_config(file_name: str):
    """
    Get logger configuration

    :param file_name str: file where to log
    :return None
    """

    return {
        "filemode": "w",
        "format": "[%(asctime)s:%(msecs)03d] %(levelname)-8s %(message)s [%(name)s]",
        "filename": os.path.join(LOGS_DIR, file_name),
        "level": logging.INFO,
        "datefmt": "%Y-%m-%d %H:%M:%S",
    }
