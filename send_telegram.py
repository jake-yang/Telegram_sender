import os
import requests
import yfinance as yf
from datetime import datetime

TOKEN = os.getenv("TELEGRAM_TOKEN")
CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

def get_finance_prices():
    tickers = {
        "BTC-USD": "BTC-USD",
        "^GSPC": "S&P 500",
        "^IXIC": "NASDAQ",
        "USDT-KRW=X": "USDT/KRW",
        "TQQQ": "TQQQ",
        "IGLD": "IGLD"
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
    finance_data = get_finance_prices()
    
    price_msg = f"⏰ {now}\n"
    # Order to match user request: BTC-USD, S&P 500, NASDAQ, USDT/KRW, TQQQ, IGLD
    order = ["BTC-USD", "S&P 500", "NASDAQ", "USDT/KRW", "TQQQ", "IGLD"]
    
    for name in order:
        if name in finance_data:
            price = finance_data[name]
            # Use appropriate formatting based on asset
            if name == "BTC-USD":
                price_msg += f"₿ BTC: ${price:,.0f}\n"
            elif name == "USDT/KRW":
                price_msg += f"💱 USDT/KRW: ₩{price:,.2f}\n"
            else:
                price_msg += f"📈 {name}: ${price:,.2f}\n"
    
    send_message(price_msg)
