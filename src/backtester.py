import pandas as pd


class Backtester:

    def __init__(
        self,
        initial_cash=100000
    ):

        self.initial_cash = initial_cash

    def run(
        self,
        df: pd.DataFrame,
        signals: list
    ):

        cash = self.initial_cash
        shares = 0

        trade_log = []
        equity_curve = []

        for i in range(len(df)):

            price = df["Close"].iloc[i]
            signal = signals[i]

            # ====================
            # BUY
            # ====================

            if signal == 1 and shares == 0:

                shares = cash // price

                if shares > 0:

                    cost = shares * price

                    cash -= cost

                    trade_log.append({
                        "Date": df.index[i],
                        "Type": "BUY",
                        "Price": price,
                        "Shares": shares
                    })

            # ====================
            # SELL
            # ====================

            elif signal == -1 and shares > 0:

                cash += shares * price

                trade_log.append({
                    "Date": df.index[i],
                    "Type": "SELL",
                    "Price": price,
                    "Shares": shares
                })

                shares = 0

            # ====================
            # Portfolio Value
            # ====================

            portfolio_value = cash + shares * price

            equity_curve.append(portfolio_value)

        # ====================
        # Final Portfolio Value
        # ====================

        final_value = (
            cash +
            shares * df["Close"].iloc[-1]
        )

        return {
            "initial_cash": self.initial_cash,
            "final_value": final_value,
            "profit": final_value - self.initial_cash,
            "trade_log": trade_log,
            "equity_curve": equity_curve
        }