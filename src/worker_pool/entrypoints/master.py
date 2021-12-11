from worker_pool.services import crawler
from worker_pool.adapters.broker import QueueBroker
from worker_pool.domain.tasks import DownloadWebsite
import os
from worker_pool import config
from worker_pool.entrypoints import worker
import threading

broker = QueueBroker()

def main():
    countries = crawler.get_countries()
      
    for country_link, country_name in countries:
        try: 
            for webs_link, webs_name in crawler.get_websites(country_link):
                broker.enqueue(DownloadWebsite(
                    link=webs_link,
                    save_path=os.path.join(config.ROOT_DIRECTORY, country_name, webs_name, ".html")
                ))
        except:
            pass
