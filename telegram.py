import requests

from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, telegram_is_configured


def send_telegram_message(message: str) -> None:
    if not telegram_is_configured():
        raise RuntimeError(
            "Telegram bot token and chat ID must be configured via environment variables."
        )

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    payload = {"chat_id": TELEGRAM_CHAT_ID, "text": message, "parse_mode": "Markdown"}
    response = requests.post(url, json=payload, timeout=10)
    response.raise_for_status()
