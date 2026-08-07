import math


def sma(values: list[float], period: int) -> list[float]:
    if len(values) < period:
        return []
    return [sum(values[i - period : i]) / period for i in range(period, len(values) + 1)]


def ema(values: list[float], period: int) -> list[float]:
    if len(values) < period:
        return []

    alpha = 2 / (period + 1)
    ema_values = [sum(values[:period]) / period]
    for price in values[period:]:
        ema_values.append((price - ema_values[-1]) * alpha + ema_values[-1])
    return ema_values


def rsi(values: list[float], period: int = 14) -> list[float]:
    if len(values) < period + 1:
        return []

    gains = []
    losses = []
    for i in range(1, len(values)):
        change = values[i] - values[i - 1]
        gains.append(max(change, 0))
        losses.append(max(-change, 0))

    avg_gain = sum(gains[:period]) / period
    avg_loss = sum(losses[:period]) / period
    rs_values = []

    if avg_loss == 0:
        rs_values.append(100.0)
    else:
        rs_values.append(100 - (100 / (1 + avg_gain / avg_loss)))

    for i in range(period, len(gains)):
        avg_gain = (avg_gain * (period - 1) + gains[i]) / period
        avg_loss = (avg_loss * (period - 1) + losses[i]) / period
        if avg_loss == 0:
            rs_values.append(100.0)
        else:
            rs_values.append(100 - (100 / (1 + avg_gain / avg_loss)))

    return rs_values


def macd(values: list[float], fast_period: int = 12, slow_period: int = 26, signal_period: int = 9) -> tuple[list[float], list[float], list[float]]:
    if len(values) < slow_period + signal_period:
        return [], [], []

    fast_ema = ema(values, fast_period)
    slow_ema = ema(values, slow_period)
    macd_line = [fast - slow for fast, slow in zip(fast_ema[-len(slow_ema) :], slow_ema)]
    signal_line = ema(macd_line, signal_period)
    histogram = [m - s for m, s in zip(macd_line[-len(signal_line) :], signal_line)]
    return macd_line[-len(signal_line) :], signal_line, histogram


def bollinger_bands(values: list[float], period: int = 20, std_dev_multiplier: float = 2.0) -> tuple[list[float], list[float], list[float]]:
    if len(values) < period:
        return [], [], []

    mid = sma(values, period)
    upper = []
    lower = []

    for i in range(period, len(values) + 1):
        window = values[i - period : i]
        mean = mid[i - period]
        variance = sum((price - mean) ** 2 for price in window) / period
        sigma = math.sqrt(variance)
        upper.append(mean + sigma * std_dev_multiplier)
        lower.append(mean - sigma * std_dev_multiplier)

    return mid, upper, lower


def atr(highs: list[float], lows: list[float], closes: list[float], period: int = 14) -> list[float]:
    if len(highs) < period + 1 or len(lows) < period + 1 or len(closes) < period + 1:
        return []

    true_ranges = []
    for i in range(1, len(closes)):
        tr = max(
            highs[i] - lows[i],
            abs(highs[i] - closes[i - 1]),
            abs(lows[i] - closes[i - 1]),
        )
        true_ranges.append(tr)

    avg_tr = sum(true_ranges[:period]) / period
    atr_values = [avg_tr]
    for tr in true_ranges[period:]:
        avg_tr = (avg_tr * (period - 1) + tr) / period
        atr_values.append(avg_tr)

    return atr_values
