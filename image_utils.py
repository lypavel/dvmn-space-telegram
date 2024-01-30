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


def get_image(image_path: Path | str) -> bytes:
    with open(image_path, "rb") as stream:
        data = stream.read()

    return data


def validate_size(image_path: Path) -> bool:
    if image_path.stat().st_size < 20971520:
        return True
    else:
        return False
