import os
import os

REDIS_CONFIG = {
    'host': '0.0.0.0',
    'port': 6379
}
REDIS_CHANNEL_NAME = 'tasks'


WORKERS = 1

RUN_FOREVER = False     # whether or not run the crawlers forever
WAIT_TIME = None        # number of seconds to wait until crawling again

BASE_URL = "https://www.alexa.com/topsites/"
ROOT_DIRECTORY = os.path.join(".", "data", "countries")

REQUESTS_TIMEOUT = 2    # requests timeout in seconds
