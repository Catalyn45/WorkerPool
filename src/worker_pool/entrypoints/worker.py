from worker_pool.adapters.broker import QueueBroker
from worker_pool.services import crawler
from concurrent import futures
from worker_pool import config


broker = QueueBroker()
from pathlib import Path

def worker():
    for task in broker.tasks():
        html_page = crawler.get_content(task.link)
        Path(task.save_path.rsplit('/', 1)[0]).mkdir(parents=True, exist_ok=True)
        with open(task.save_path, 'w') as f:
            f.write(html_page)


if __name__ == '__main__':
    with futures.ThreadPoolExecutor() as pool:
        result_futures = [pool.submit(worker) for i in range(config.WORKERS)]

        while True:
            done, not_done = futures.wait(result_futures, return_when=futures.FIRST_COMPLETED)
            result_futures = not_done
            