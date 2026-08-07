import time
from dotenv import load_dotenv
from datetime import datetime, timedelta
load_dotenv()
from config import ALERT_CONFIDENCE_THRESHOLD, telegram_is_configured
from fetcher import fetch_klines
from signal import build_signal
from telegram import send_telegram_message


def seconds_until_next_15min() -> float:
    now = datetime.utcnow()
    next_minute = ((now.minute // 15) + 1) * 15
    if next_minute == 60:
        next_run = now.replace(hour=(now.hour + 1) % 24, minute=0, second=0, microsecond=0)
    else:
        next_run = now.replace(minute=next_minute, second=0, microsecond=0)
    delay = (next_run - now).total_seconds()
    return max(delay, 0)


def format_message(signal: dict) -> str:
    reasons = signal.get("reasons", [])
    reason_text = " | ".join(reasons[:4]) if reasons else "Technical signal generated."
    return (
        f"*BTC Alert — {signal['direction']}*\n"
        f"Timestamp: {signal['timestamp']}\n"
        f"Price: `${signal['current_price']}`\n"
        f"Entry: `${signal['entry_price']}`\n"
        f"Stop Loss: `${signal['stop_loss']}`\n"
        f"Take Profit: `${signal['take_profit']}`\n"
        f"Confidence: *{signal['confidence']}%*\n"
        f"RSI(14): {signal['rsi']} | MACD hist: {signal['macd_hist']}\n"
        f"EMA20: {signal['ema20']} | EMA50: {signal['ema50']}\n"
        f"BB upper: {signal['bb_upper']} | BB lower: {signal['bb_lower']}\n"
        f"ATR(14): {signal['atr']}\n"
        f"Volume: {signal['volume']} | Avg: {signal['volume_ma']}\n"
        f"_Why: {reason_text}_"
    )


def run_bot() -> None:
    print("Starting BTC alert bot for Kalshi 15-minute markets.")
    print(f"Telegram configured: {telegram_is_configured()}")

    while True:
        now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC")
        try:
            klines = fetch_klines()
            signal = build_signal(klines)

            if signal["confidence"] >= ALERT_CONFIDENCE_THRESHOLD:
                message = format_message(signal)
                send_telegram_message(message)
                if telegram_is_configured():
                    send_telegram_message(message)
                    print(f"[{now}] Sent alert to Telegram: {signal['direction']} {signal['confidence']}%")
                else:
                    print(f"[{now}] Alert ready but Telegram not configured.")
                    print(message)
            else:
                print(f"[{now}] No alert: confidence {signal['confidence']}% below threshold.")
        except Exception as error:
            print(f"[{now}] Error generating signal: {error}")

        sleep_seconds = seconds_until_next_15min()
        print(f"Waiting {int(sleep_seconds)} seconds until next 15-minute candle cycle.")
        time.sleep(sleep_seconds)


if __name__ == "__main__":
    run_bot()
