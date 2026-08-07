import requests
from datetime import datetime

from config import BINANCE_KLINES_URL, SYMBOL, INTERVAL, LIMIT, REQUEST_TIMEOUT


def fetch_klines(limit: int = LIMIT) -> list[dict]:
    params = {"symbol": SYMBOL, "interval": INTERVAL, "limit": limit}
    response = requests.get(BINANCE_KLINES_URL, params=params, timeout=REQUEST_TIMEOUT)
    response.raise_for_status()
    raw = response.json()
    candles = []

    for item in raw:
        candles.append(
            {
                "open_time": datetime.utcfromtimestamp(item[0] / 1000),
                "open": float(item[1]),
                "high": float(item[2]),
                "low": float(item[3]),
                "close": float(item[4]),
                "volume": float(item[5]),
            }
        )

    return candles


def get_latest_price(klines: list[dict]) -> float:
    return float(klines[-1]["close"])
