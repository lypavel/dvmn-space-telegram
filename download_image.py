import os
import requests as rq
from urllib.parse import urlsplit, unquote
from pathlib import Path


def download_image(url: str, file_path: str, payload: dict = None) -> None:
    if not payload:
        payload = {}

    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    response = rq.get(url, params=payload)
    response.raise_for_status()

    with open(file_path, "wb") as stream:
        stream.write(response.content)


def get_file_extension(url: str) -> str:
    file_path = unquote(urlsplit(url).path)
    _, full_name = os.path.split(file_path)
    _, extension = os.path.splitext(full_name)

    return extension