import telegram
import os
import argparse
import time
from dotenv import load_dotenv
from pathlib import Path
from random import shuffle
from download_image import get_image


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
        help="Time between posting images in seconds."
    )

    return parser


def main() -> None:
    load_dotenv()

    parser = create_parser()
    args = parser.parse_args()

    chat_id = args.chat_id
    cooldown = args.cooldown

    if not cooldown:
        cooldown = 3

    bot = telegram.Bot(token=os.environ["TG_BOT_TOKEN"])

    images = [image for image in Path("images/").iterdir()]

    while True:
        shuffle(images)

        for image_path in images:
            # if image size > 20 MB
            if image_path.stat().st_size >= 20971520:
                continue

            image = get_image(image_path)

            bot.send_photo(photo=image, chat_id=chat_id)

            time.sleep(cooldown)


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as dir_not_found:
        exit(f"Директория с изображениями не найдена:\n{dir_not_found}")
