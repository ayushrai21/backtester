import pandas as pd
import numpy as np


class Backtester:
    def __init__(self, initial_cash=100000):
        self.initial_cash = initial_cash

    def run(self, df: pd.DataFrame, signals: list):

        cash = self.initial_cash
        shares = 0

        trade_log = []
        equity_curve = []

        # Extract to NumPy arrays before looping to avoid slow .iloc lookups
        prices = df["Close"].to_numpy()
        dates = df.index.astype(str).to_numpy()

        for i in range(len(prices)):
            price = float(prices[i])
            signal = signals[i]

            # buy signal
            if signal == 1 and shares == 0:
                shares = int(cash // price)
                if shares > 0:
                    cost = shares * price
                    cash -= cost
                    trade_log.append(
                        {
                            "Date": dates[i],
                            "Type": "BUY",
                            "Price": price,
                            "Shares": shares,
                        }
                    )

            # sell signal
            elif signal == -1 and shares > 0:
                cash += shares * price
                trade_log.append(
                    {
                        "Date": dates[i],
                        "Type": "SELL",
                        "Price": price,
                        "Shares": shares,
                    }
                )

                shares = 0

            portfolio_value = cash + shares * price
            equity_curve.append(float(portfolio_value))

        final_value = cash + shares * float(prices[-1])

        return {
            "initial_cash": float(self.initial_cash),
            "final_value": float(final_value),
            "profit": float(final_value - self.initial_cash),
            "trade_log": trade_log,
            "equity_curve": equity_curve,
        }