import pandas as pd


class SMACrossoverStrategy:
    """
    Buy when Fast SMA > Slow SMA
    Sell when Fast SMA < Slow SMA
    """

    def __init__(self, fast_period=10, slow_period=50):

        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signals(self, df: pd.DataFrame) -> list:

        signals = []

        fast_col = f"SMA{self.fast_period}"
        slow_col = f"SMA{self.slow_period}"

        for i in range(len(df)):
            sma_fast = df[fast_col].iloc[i]
            sma_slow = df[slow_col].iloc[i]

            if pd.isna(sma_fast) or pd.isna(sma_slow):
                signals.append(0)

            elif sma_fast > sma_slow:
                signals.append(1)

            else:
                signals.append(-1)

        return signals


class RSIStrategy:
    """
    Buy when RSI < 30
    Sell when RSI > 70
    Hold otherwise
    """

    def generate_signals(self, df: pd.DataFrame) -> list:

        signals = []

        for rsi in df["RSI"]:
            if pd.isna(rsi):
                signals.append(0)

            elif rsi < 30:
                signals.append(1)

            elif rsi > 70:
                signals.append(-1)

            else:
                signals.append(0)

        return signals


class MACDStrategy:
    """
    Buy when MACD > Signal Line
    Sell when MACD < Signal Line
    """

    def generate_signals(self, df: pd.DataFrame) -> list:

        signals = []

        for i in range(len(df)):
            macd = df["MACD"].iloc[i]
            signal = df["MACD_SIGNAL"].iloc[i]

            if pd.isna(macd) or pd.isna(signal):
                signals.append(0)

            elif macd > signal:
                signals.append(1)

            else:
                signals.append(-1)

        return signals


class BollingerStrategy:
    """
    Buy when price touches lower band
    Sell when price touches upper band
    """

    def generate_signals(self, df: pd.DataFrame) -> list:

        signals = []

        for i in range(len(df)):
            close = df["Close"].iloc[i]
            upper = df["BB_UPPER"].iloc[i]
            lower = df["BB_LOWER"].iloc[i]

            if pd.isna(upper) or pd.isna(lower):
                signals.append(0)

            elif close < lower:
                signals.append(1)

            elif close > upper:
                signals.append(-1)

            else:
                signals.append(0)

        return signals


class PriceAboveSMAStrategy:
    """
    Buy when Close > SMA50
    Sell when Close < SMA50
    """

    def generate_signals(self, df: pd.DataFrame) -> list:

        signals = []

        for i in range(len(df)):
            close = df["Close"].iloc[i]
            sma50 = df["SMA50"].iloc[i]

            if pd.isna(sma50):
                signals.append(0)

            elif close > sma50:
                signals.append(1)

            else:
                signals.append(-1)

        return signals


class EMACrossoverStrategy:
    """
    Buy when EMA20 > EMA100
    Sell when EMA20 < EMA100
    """

    def generate_signals(self, df: pd.DataFrame) -> list:

        signals = []

        for i in range(len(df)):
            ema_fast = df["EMA20"].iloc[i]
            ema_slow = df["EMA100"].iloc[i]

            if pd.isna(ema_fast) or pd.isna(ema_slow):
                signals.append(0)

            elif ema_fast > ema_slow:
                signals.append(1)

            else:
                signals.append(-1)

        return signals
