from abc import ABC, abstractmethod
import pickle
from typing import Iterable
from worker_pool import config
from worker_pool.domain.tasks import DownloadWebsite
import redis
import logging

from worker_pool.exceptions.pool_exceptions import BrokerTimedOut

logger = logging.getLogger(__name__)


class Broker(ABC):
    @abstractmethod
    def enqueue(self, task):
        raise NotImplementedError()

    @abstractmethod
    def tasks(self):
        raise NotImplementedError()


class RedisBroker(Broker):
    def __init__(self) -> None:
        logger.info("initiating redis connection")
        self.connection = redis.Redis(**config.REDIS_CONFIG)

    def enqueue(self, task: DownloadWebsite):
        """
        Enqueue a task into the redis queue

        :param task DownloadWebsite the task to be enqueued
        :return None
        """

        logger.info(f"enqueueing task: {task}")
        self.connection.lpush(config.REDIS_CHANNEL_NAME, pickle.dumps(task))

    def tasks(self) -> Iterable[DownloadWebsite]:
        """
        Gen an iterator for the enqueued tasks

        :return Iterable[DownloadWebsite]: the iterator for the enqueued tasks
        """
        while True:
            try:
                task = pickle.loads(
                    self.connection.brpop(config.REDIS_CHANNEL_NAME, timeout=15)[1]
                )
            except redis.exceptions.TimeoutError:
                raise BrokerTimedOut()

            logger.info(f"got task from queue: {task}")
            yield task
