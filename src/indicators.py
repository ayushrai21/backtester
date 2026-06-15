import pandas as pd


def sma(df: pd.DataFrame, period: int) -> pd.Series:
    """
    Simple Moving Average
    """

    return (
        df["Close"].rolling(window=period).mean()
    )


def ema(df: pd.DataFrame, period: int) -> pd.Series:
    """
    Exponential Moving Average
    """

    return (
        df["Close"].ewm(span=period, adjust=False).mean()
    )


def rsi(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """
    Relative Strength Index
    """

    delta = df["Close"].diff()

    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    avg_gain = gain.rolling(period).mean()
    avg_loss = loss.rolling(period).mean()

    rs = avg_gain / avg_loss

    return 100 - (100 / (1 + rs))


def macd(
    df: pd.DataFrame,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9
):
    """
    MACD Line and Signal Line
    """

    ema_fast = ema(df, fast_period)
    ema_slow = ema(df, slow_period)

    macd_line = ema_fast - ema_slow

    signal_line = (
        macd_line.ewm(span=signal_period, adjust=False).mean()
    )

    histogram = macd_line - signal_line

    return macd_line, signal_line, histogram


def bollinger_bands(
    df: pd.DataFrame,
    period: int = 20,
    std_multiplier: int = 2
):
    """
    Bollinger Bands
    """

    middle_band = sma(df, period)

    rolling_std = (
        df["Close"].rolling(period).std()
    )

    upper_band = (
        middle_band + std_multiplier * rolling_std
    )

    lower_band = (
        middle_band - std_multiplier * rolling_std
    )

    return upper_band, middle_band, lower_band