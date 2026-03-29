import os
import requests
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_prices():
    url = "https://api.coingecko.com/api/v3/simple/price"
    params = {
        "ids": "bitcoin,tether",
        "vs_currencies": "usd,krw"
    }

    res = requests.get(url, params=params).json()

    btc_usd = res["bitcoin"]["usd"]
    usdt_krw = res["tether"]["krw"]

    return btc_usd, usdt_krw

def send_message(text):
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text
    })

if __name__ == "__main__":
    btc, usdt = get_prices()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    message = f"""⏰ {now}
₿ BTC: ${btc:,}
💱 USDT/KRW: ₩{usdt:,}
"""

    send_message(message)
