import telegram
import os
import argparse
from dotenv import load_dotenv
from pathlib import Path
from random import choice
from download_image import get_image, validate_size


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="\
            Uploads random or specified image \
            in telegram channel.\
        "
    )
    parser.add_argument("chat_id", help="Telegram chat id.")
    parser.add_argument("--image_name", help="Image name.")

    return parser


def specify_image(image_name) -> bytes:
    if not image_name:
        images = [image for image in Path("images/").iterdir()]

        image = choice(images)
    else:
        image = Path("images/") / image_name

    if not validate_size(image):
        return

    return get_image(image)


def main() -> None:
    load_dotenv()

    parser = create_parser()
    args = parser.parse_args()

    chat_id = args.chat_id
    image_name = args.image_path

    bot = telegram.Bot(token=os.environ["TG_BOT_TOKEN"])

    image = specify_image(image_name)
    if image:
        bot.send_photo(photo=image, chat_id=chat_id)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError() as img_not_found:
        exit(f"Изображение не найдено:\n{img_not_found}")
