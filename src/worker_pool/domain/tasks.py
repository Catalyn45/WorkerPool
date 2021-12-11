from dataclasses import dataclass


@dataclass
class DownloadWebsite:
    link: str
    save_path: str
