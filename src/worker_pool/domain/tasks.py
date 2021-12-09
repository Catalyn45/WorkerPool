from dataclasses import dataclass

@dataclass
class Task:
    pass

@dataclass
class DownloadWebsite(Task):
    link: str
    save_path: str

# gracefully shut down the workers
@dataclass
class ShutDown(Task):
    message: str
