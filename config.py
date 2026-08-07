import os

BINANCE_KLINES_URL = "https://api.binance.us/api/v3/klines"
SYMBOL = "BTCUSD"
INTERVAL = "15m"
LIMIT = 100

TELEGRAM_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")
ALERT_CONFIDENCE_THRESHOLD = 65
REQUEST_TIMEOUT = 10


def telegram_is_configured() -> bool:
    return TELEGRAM_BOT_TOKEN not in (None, "", "<YOUR_TELEGRAM_BOT_TOKEN>") and TELEGRAM_CHAT_ID not in (None, "", "<YOUR_TELEGRAM_CHAT_ID>")
