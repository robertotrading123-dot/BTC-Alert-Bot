# BTC Alert Bot for Kalshi 15-Minute Markets

This bot fetches Binance BTCUSDT 15-minute candles, analyzes RSI, MACD, EMA20, EMA50, Bollinger Bands, ATR, and volume, and sends alerts to Telegram when confidence reaches 75% or higher.

## Files

- `main.py` - entrypoint and scheduler
- `config.py` - environment configuration
- `fetcher.py` - Binance candle downloader
- `indicators.py` - technical indicator calculations
- `signal.py` - signal scoring and alert generation
- `telegram.py` - Telegram notification sender
- `requirements.txt` - Python dependencies

## Requirements

- Python 3.11+
- `requests`

## Installation

1. Create a Python environment:
   ```bash
   python -m venv venv
   venv\Scripts\Activate.ps1
   pip install -r requirements.txt
   ```

2. Set environment variables:
   - `TELEGRAM_BOT_TOKEN`
   - `TELEGRAM_CHAT_ID`

   Example PowerShell:
   ```powershell
   $env:TELEGRAM_BOT_TOKEN = "123456:ABCDEF"
   $env:TELEGRAM_CHAT_ID = "-1001234567890"
   ```

## Usage

Run the bot:

```powershell
python main.py
```

The bot checks Binance BTCUSDT 15-minute candles and sends a Telegram message when the confidence score is at least 75%.

## Alert contents

Alerts include:

- BUY or SELL
- Current BTC price
- Suggested entry price
- Stop Loss
- Take Profit
- Confidence %
- Brief rationale for the signal

## Notes

- The bot aligns its schedule to the next 15-minute candle boundary.
- Use this bot for informational signals only; it is not financial advice.
