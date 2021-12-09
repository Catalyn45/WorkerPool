from abc import ABC, abstractmethod

class Broker(ABC):
    @abstractmethod
    def enqueue(self, task):
        raise NotImplementedError()

    @abstractmethod
    def tasks(self):
        raise NotImplementedError()


class RedisBroker(Broker):
    def enqueue(self, task):
        print(task)

    def tasks(self):
        pass
