from typing import Set
from worker_pool.adapters.broker import RedisBroker
from worker_pool.services import crawler, file
import multiprocessing
from multiprocessing.connection import wait
from worker_pool import config
from worker_pool.exceptions.pool_exceptions import (
    CrawlingException,
    FileError,
)
import logging
from itertools import product


def worker(logger: logging.Logger):
    """
    The worker who get the tasks from the queue and download the pages

    :param logger: logging.Logger: the logger passed to avoid race conditions
    """

    broker = RedisBroker()
    for task in broker.tasks():
        try:
            logger.info(f"getting the html content from link: {task.link}")
            html_page = crawler.get_content(task.link)

            logger.info(f"saving the html content to file: {task.save_path}")
            file.create_file(task.save_path, html_page)
        except (CrawlingException, FileError) as e:
            logger.warning(f"Exception durring task handling: {str(e)}")


def main():
    logging.basicConfig(**config.get_logger_config("workers_logs.txt"))
    logger = logging.getLogger(__name__)

    processes: Set[multiprocessing.Process] = set()

    try:
        for i in range(config.WORKERS):
            process = multiprocessing.Process(target=worker, args=(logger,))
            logger.info(f"starting worker number: {i}")
            process.start()
            processes.add(process)

        logger.info("all workers started")

        while True:
            ready = wait({process.sentinel for process in processes})

            ready_processes = set()
            for sentinel, process in product(ready, processes):
                if process.sentinel != sentinel:
                    continue

                process.join()
                ready_processes.add(process)

            processes.difference_update(
                {process for process in processes if process.sentinel in ready}
            )

            # restart worker if dead
            for i in range(len(ready)):
                logger.warning("worker dead, restarting")
                process = multiprocessing.Process(target=worker, args=(logger,))

                logger.info("sarting worker")
                process.start()
                processes.add(process)

    except KeyboardInterrupt:
        logger.info("closing workers")
        for process in processes:
            logger.info(f"terminating worker")
            process.terminate()
    except Exception as e:
        logger.error(f"unexpected error occureed: {str(e)}, killing workers")
        for process in processes:
            process.terminate()


if __name__ == "__main__":
    main()
