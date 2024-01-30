import requests as rq
import os
from image_utils import download_image
from datetime import datetime as dt
from dotenv import load_dotenv


def fetch_nasa_epic(api_token: str) -> None:
    payload = {
        "api_key": api_token
    }

    api_url = "https://api.nasa.gov/EPIC/api/natural/images"

    response = rq.get(api_url, params=payload)
    response.raise_for_status()

    for index, epic_image in enumerate(response.json()):
        name = f"{epic_image['image']}.png"

        full_date = dt.strptime(epic_image["date"], "%Y-%m-%d %H:%M:%S").date()
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

    nasa_token = os.environ["NASA_TOKEN"]

    try:
        fetch_nasa_epic(nasa_token)
    except rq.exceptions.HTTPError as http_error:
        exit(f"Ошибка подключения к серверу:\n{http_error}")


if __name__ == "__main__":
    main()
