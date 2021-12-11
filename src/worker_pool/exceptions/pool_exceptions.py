class WorkerPoolException(Exception):
    def __init__(self, message="Worker pool exception") -> None:
        super().__init__(message)


class CrawlingException(WorkerPoolException):
    def __init__(self, message="Crawling exception") -> None:
        super().__init__(message=message)


class BrokerTimedOut(WorkerPoolException):
    def __init__(self, message="Broker timed out") -> None:
        super().__init__(message=message)


class CrawlerTimedOut(CrawlingException):
    def __init__(self, message="Crawler timed out") -> None:
        super().__init__(message=message)


class FileError(WorkerPoolException):
    def __init__(self, message="File error") -> None:
        super().__init__(message=message)
