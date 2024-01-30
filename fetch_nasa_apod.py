import requests as rq
import os
import argparse
from dotenv import load_dotenv
from image_utils import get_file_extension, download_image


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="\
            Downloads APOD images from NASA \
            in desired count.\
        "
    )
    parser.add_argument(
        "--count",
        default=1,
        help="Number of images to download.",
        type=int,
    )

    return parser


def fetch_nasa_apod(count: int = 1) -> None:
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


def main() -> None:
    load_dotenv()

    parser = create_parser()
    args = parser.parse_args()

    count = args.count

    try:
        fetch_nasa_apod(count)
    except rq.exceptions.HTTPError as http_error:
        exit(f"Ошибка подключения к серверу:\n{http_error}")


if __name__ == "__main__":
    main()
