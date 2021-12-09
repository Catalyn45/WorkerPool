class WorkerPoolException(Exception):
    def __init__(self, message="Worker pool exception") -> None:
        super().__init__(message=message)


class CrawlingException(Exception):
    def __init__(self, message="Crawling exception") -> None:
        super().__init__(message=message)
