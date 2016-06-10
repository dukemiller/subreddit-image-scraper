from urllib.request import urlretrieve
import os.path as path
import handlers
import tools


def get_download_url_for(url: str) -> str:
    pass


def download(url: str, output_path: str) -> bool:
    download_path = path.join(output_path, tools.get_url_filename(url))
    if not path.exists(download_path):
        urlretrieve(url, download_path)
        return True
    return False
