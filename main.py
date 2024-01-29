import requests as rq
from pathlib import Path
import os
from datetime import datetime as dt
from urllib.parse import urlsplit, unquote
from dotenv import load_dotenv


def download_image(url: str, file_path: str, payload: dict = None) -> None:
    if not payload:
        payload = {}

    file_path = Path(file_path)
    file_path.parent.mkdir(parents=True, exist_ok=True)

    response = rq.get(url, params=payload)
    response.raise_for_status()

    with open(file_path, "wb") as stream:
        stream.write(response.content)


def fetch_spacex_launch(launch_id: str = None) -> None:
    if launch_id:
        api_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    else:
        api_url = "https://api.spacexdata.com/v5/launches/latest"

    response = rq.get(api_url)
    response.raise_for_status()

    launch_images = response.json()["links"]["flickr"]["original"]

    for index, image in enumerate(launch_images):
        download_image(image, f"images/spacex_{index}.jpeg")


def fetch_nasa_apod(count: int = None) -> None:
    if not count:
        count = 1

    payload = {
        "api_key": os.environ["NASA_TOKEN"],
        "count": count
    }

    api_url = "https://api.nasa.gov/planetary/apod"

    response = rq.get(api_url, params=payload)
    response.raise_for_status()

    images = [image["url"] for image in response.json()]

    for index, image_link in enumerate(images):
        extension = (get_file_extension(image_link))
        if not extension:
            continue

        download_image(image_link, f"images/nasa_apod_{index}{extension}")


def fetch_nasa_epic() -> None:
    payload = {
        "api_key": os.environ["NASA_TOKEN"]
    }

    api_url = "https://api.nasa.gov/EPIC/api/natural/images"

    response = rq.get(api_url, params=payload)
    response.raise_for_status()

    for index, image_info in enumerate(response.json()):
        name = f"{image_info['image']}.png"

        full_date = dt.strptime(image_info["date"], "%Y-%m-%d %H:%M:%S").date()
        day, month, year = full_date.day, full_date.month, full_date.year

        image_link = f"{year}/{month:02}/{day:02}/png/{name}"

        full_link = f"https://api.nasa.gov/EPIC/archive/natural/{image_link}"

        download_image(
            full_link,
            f"images/nasa_epic_{index}.png",
            payload=payload
        )


def get_file_extension(url: str) -> str:
    file_path = unquote(urlsplit(url).path)
    _, full_name = os.path.split(file_path)
    _, extension = os.path.splitext(full_name)

    return extension


def main() -> None:
    load_dotenv()
    fetch_spacex_launch()
    fetch_nasa_apod()
    fetch_nasa_epic()


if __name__ == "__main__":
    try:
        main()
    except rq.exceptions.HTTPError as http_error:
        print(http_error)
