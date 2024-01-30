import telegram
import os
from dotenv import load_dotenv


def main(chat_id: str) -> None:
    load_dotenv()

    bot = telegram.Bot(token=os.environ["TG_BOT_TOKEN"])

    bot.send_message(text="Hello", chat_id=chat_id)

    with open("images/nasa_apod_0.jpg", "rb") as stream:
        data = stream.read()

    bot.send_photo(photo=data, chat_id=chat_id)


if __name__ == "__main__":
    main("@lypavel_dvmn_space")
