from pathlib import Path
import os
from worker_pool.exceptions.pool_exceptions import FileError


def create_file(file_name: str, content: str):
    """
    Create a file an write the content in it (the directories until it will be created if not exists)

    :param file_name str: the file name
    :param content str: the content
    :return None
    """

    try:
        # create the directories until the file name if not exist
        Path(os.path.split(file_name)[0]).mkdir(parents=True, exist_ok=True)

        with open(file_name, "w") as f:
            f.write(content)
    except FileNotFoundError as e:
        raise FileError(str(e))
