import telegram
import os
import argparse
import time
from dotenv import load_dotenv
from pathlib import Path
from random import shuffle
from image_utils import get_image, validate_size


def create_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="\
            Uploads all images from \"images\\\" directory \
            in Telegram with specified cooldown. \
        "
    )
    parser.add_argument("chat_id", help="Telegram chat id.")
    parser.add_argument(
        "-cd",
        "--cooldown",
        default=14440,
        help="Time between posting images in seconds.",
        type=int
    )

    return parser


def main() -> None:
    load_dotenv()

    parser = create_parser()
    args = parser.parse_args()

    chat_id = args.chat_id
    cooldown = args.cooldown

    bot = telegram.Bot(token=os.environ["TG_BOT_TOKEN"])

    images = [image for image in Path("images/").iterdir()]

    while True:
        shuffle(images)

        for image_path in images:
            if not validate_size(image_path):
                continue

            image = get_image(image_path)

            bot.send_photo(photo=image, chat_id=chat_id)

            time.sleep(cooldown)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as dir_not_found:
        exit(f"Директория с изображениями не найдена:\n{dir_not_found}")
    except telegram.error.NetworkError as net_error:
        print(f"Во время загрузки произошла ошибка:\n{net_error}")
