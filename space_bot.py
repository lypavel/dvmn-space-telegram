import telegram
import os
from dotenv import load_dotenv


def main(chat_id: str) -> None:
    load_dotenv()

    bot = telegram.Bot(token=os.environ["TG_BOT_TOKEN"])

    bot.send_message(text="Hello", chat_id=chat_id)


if __name__ == "__main__":
    main("@lypavel_dvmn_space")
