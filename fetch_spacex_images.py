import requests as rq
from image_utils import download_image
import argparse


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="\
            Downloads photos of latest or specific \
            SpaceX launch if they were made.\
        "
    )
    parser.add_argument("--launch_id", help="Id of specific rocket launch.")

    return parser


def fetch_spacex_images(launch_id) -> None:
    if launch_id:
        api_url = f"https://api.spacexdata.com/v5/launches/{launch_id}"
    else:
        api_url = "https://api.spacexdata.com/v5/launches/latest"

    response = rq.get(api_url)
    response.raise_for_status()

    launch_images = response.json()["links"]["flickr"]["original"]

    for index, image in enumerate(launch_images):
        download_image(image, f"images/spacex_{index}.jpeg")


def main() -> None:
    parser = create_parser()
    args = parser.parse_args()

    launch_id = args.launch_id

    try:
        fetch_spacex_images(launch_id)
    except rq.exceptions.HTTPError as http_error:
        exit(f"Ошибка подключения к серверу:\n{http_error}")


if __name__ == "__main__":
    main()
