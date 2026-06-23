import pandas as pd
import numpy as np

class SMACrossoverStrategy:
    """
    Buy when Fast SMA > Slow SMA
    Sell when Fast SMA < Slow SMA
    """

    def __init__(self, fast_period=10, slow_period=50):

        self.fast_period = fast_period
        self.slow_period = slow_period

    def generate_signals(self, df: pd.DataFrame) -> list:
        fast_col = f"SMA{self.fast_period}"
        slow_col = f"SMA{self.slow_period}"

        signals = np.where(df[fast_col] > df[slow_col], 1, -1)
        signals[df[fast_col].isna() | df[slow_col].isna()] = 0

        return signals.tolist()


class RSIStrategy:
    """
    Buy when RSI < 30
    Sell when RSI > 70
    Hold otherwise
    """

    def generate_signals(self, df: pd.DataFrame) -> list:
        signals = np.zeros(len(df))
        signals = np.where(df["RSI"] < 30, 1, signals)
        signals = np.where(df["RSI"] > 70, -1, signals)

        signals[df['RSI'].isna()] = 0
        return signals.tolist()


class MACDStrategy:
    """
    Buy when MACD > Signal Line
    Sell when MACD < Signal Line
    """

    def generate_signals(self, df: pd.DataFrame) -> list:
        signals = np.where(df["MACD"] > df["MACD_SIGNAL"], 1, -1)
        signals[df["MACD"].isna() | df["MACD_SIGNAL"].isna()] = 0
        return signals.tolist()


class BollingerStrategy:
    """
    Buy when price touches lower band
    Sell when price touches upper band
    """

    def generate_signals(self, df: pd.DataFrame) -> list:
        close = df["Close"]
        signals = np.zeros(len(df))
        
        signals = np.where(close < df["BB_LOWER"], 1, signals)
        signals = np.where(close > df["BB_UPPER"], -1, signals)
        
        signals[df["BB_UPPER"].isna()] = 0
        return signals.tolist()


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
