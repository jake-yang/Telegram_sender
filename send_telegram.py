import os
import requests
import yfinance as yf
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_crypto_prices():
    try:
        url = "https://api.coingecko.com/api/v3/simple/price"
        params = {
            "ids": "bitcoin,tether",
            "vs_currencies": "usd,krw"
        }
        res = requests.get(url, params=params).json()
        btc_usd = res["bitcoin"]["usd"]
        usdt_krw = res["tether"]["krw"]
        return btc_usd, usdt_krw
    except Exception as e:
        print(f"Error fetching crypto: {e}")
        return None, None

def get_finance_prices():
    tickers = {
        "NQ=F": "NASDAQ Futures",
        "TQQQ": "TQQQ",
        "BZ=F": "Brent Oil",
        "IGLD": "IGLD",
        "QQQ": "QQQ"
    }
    results = {}
    try:
        for symbol, name in tickers.items():
            ticker = yf.Ticker(symbol)
            hist = ticker.history(period="1d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]
                results[name] = price
            else:
                print(f"No history found for {symbol}")
        return results
    except Exception as e:
        print(f"Error fetching finance data: {e}")
        return {}

def send_message(text):
    if not TOKEN or not CHAT_ID:
        print("Telegram configuration missing.")
        return
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
    requests.post(url, data={
        "chat_id": CHAT_ID,
        "text": text,
        "disable_web_page_preview": "false"
    })

if __name__ == "__main__":
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    # Prices
    btc, usdt = get_crypto_prices()
    finance_data = get_finance_prices()
    
    price_msg = f"⏰ {now}\n"
    if btc:
        price_msg += f"₿ BTC: ${btc:,}\n"
    if usdt:
        price_msg += f"💱 USDT/KRW: ₩{usdt:,}\n"
    
    for name, price in finance_data.items():
        price_msg += f"📈 {name}: ${price:,.2f}\n"
    
    send_message(price_msg)
