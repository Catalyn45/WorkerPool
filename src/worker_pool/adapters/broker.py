from abc import ABC, abstractmethod
import queue
import pickle
from worker_pool.domain.tasks import DownloadWebsite

class Broker(ABC):
    @abstractmethod
    def enqueue(self, task):
        raise NotImplementedError()

    @abstractmethod
    def tasks(self):
        raise NotImplementedError()


class QueueBroker(Broker):
    queue = queue.Queue(maxsize=100)

    def enqueue(self, task: DownloadWebsite):
        self.queue.put(pickle.dumps(task))

    def tasks(self):
        while self.queue:
            print('getting from queue')
            yield pickle.loads(self.queue.get(block=True))

class RedisBroker(Broker):
    def enqueue(self, task: DownloadWebsite):
        pass

    def tasks(self):
        pass
