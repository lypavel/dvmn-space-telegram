import requests as rq
import os
from download_image import download_image
from datetime import datetime as dt
from dotenv import load_dotenv


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


def main() -> None:
    load_dotenv()

    fetch_nasa_epic()


if __name__ == "__main__":
    try:
        main()
    except rq.exceptions.HTTPError as http_error:
        exit(f"Ошибка подключения к серверу:\n{http_error}")
