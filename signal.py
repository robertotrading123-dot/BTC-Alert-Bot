from datetime import datetime

from indicators import atr, bollinger_bands, ema, macd, rsi, sma


def build_signal(klines: list[dict]) -> dict:
    closes = [item["close"] for item in klines]
    highs = [item["high"] for item in klines]
    lows = [item["low"] for item in klines]
    volumes = [item["volume"] for item in klines]

    if len(closes) < 50:
        raise ValueError("Need at least 50 candles for the indicator calculations.")

    ema20 = ema(closes, 20)[-1]
    ema50 = ema(closes, 50)[-1]
    rsi14 = rsi(closes, 14)[-1]
    macd_line, signal_line, hist = macd(closes)
    macd_value = macd_line[-1]
    macd_signal = signal_line[-1]
    macd_hist = hist[-1]
    bb_mid, bb_upper, bb_lower = bollinger_bands(closes, 20)
    bb_mid_value = bb_mid[-1]
    bb_upper_value = bb_upper[-1]
    bb_lower_value = bb_lower[-1]
    atr_values = atr(highs, lows, closes, 14)
    atr_value = atr_values[-1]
    atr_ma = sma(atr_values, 14)[-1] if len(atr_values) >= 14 else atr_value
    volume_ma = sma(volumes, 20)[-1]
    last_close = closes[-1]
    previous_close = closes[-2]

    score = 0
    reasons = []

    if ema20 > ema50:
        score += 20
        reasons.append("EMA20 above EMA50")
    else:
        score -= 20
        reasons.append("EMA20 below EMA50")

    if macd_hist > 0 and macd_value > macd_signal:
        score += 20
        reasons.append("MACD bullish momentum")
    elif macd_hist < 0 and macd_value < macd_signal:
        score -= 20
        reasons.append("MACD bearish momentum")
    else:
        reasons.append("MACD is neutral")

    if rsi14 >= 60:
        score += 15
        reasons.append("RSI in bullish range")
    elif rsi14 <= 40:
        score -= 15
        reasons.append("RSI in bearish range")
    else:
        reasons.append("RSI is neutral")

    if last_close > bb_mid_value:
        score += 10
        reasons.append("Price above Bollinger mid-band")
    else:
        score -= 10
        reasons.append("Price below Bollinger mid-band")

    if last_close > bb_upper_value:
        score += 5
        reasons.append("Price is above the upper Bollinger band")
    elif last_close < bb_lower_value:
        score -= 5
        reasons.append("Price is below the lower Bollinger band")
    else:
        reasons.append("Price inside the Bollinger bands")

    if volumes[-1] > volume_ma:
        score += 10
        reasons.append("Volume above the 20-period average")
    else:
        score -= 5
        reasons.append("Volume below the 20-period average")

    if atr_value >= atr_ma:
        score += 10
        reasons.append("Volatility is above average")
    else:
        reasons.append("Volatility is below average")

    if last_close > previous_close:
        score += 10
        reasons.append("Price is pushing higher")
    else:
        score -= 10
        reasons.append("Price is pushing lower")

    direction = "BUY" if score >= 0 else "SELL"
    confidence = min(100, max(0, abs(score)))

    entry_price = round(last_close, 2)
    stop_loss = round(last_close - atr_value * 1.5, 2) if direction == "BUY" else round(last_close + atr_value * 1.5, 2)
    take_profit = round(last_close + atr_value * 3, 2) if direction == "BUY" else round(last_close - atr_value * 3, 2)

    return {
        "direction": direction,
        "current_price": round(last_close, 2),
        "entry_price": entry_price,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "confidence": confidence,
        "rsi": round(rsi14, 1),
        "macd_hist": round(macd_hist, 5),
        "ema20": round(ema20, 2),
        "ema50": round(ema50, 2),
        "bb_upper": round(bb_upper_value, 2),
        "bb_lower": round(bb_lower_value, 2),
        "atr": round(atr_value, 4),
        "volume": round(volumes[-1], 2),
        "volume_ma": round(volume_ma, 2),
        "reasons": reasons,
        "timestamp": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S UTC"),
    }
