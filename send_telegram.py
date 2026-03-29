import os
import requests

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")


def send_message():
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"

    res = requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": "🚀 GitHub Actions test success"
    })

    print(res.text)


if __name__ == "__main__":
    send_message()