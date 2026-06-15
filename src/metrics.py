# src/metrics.py

import numpy as np
import pandas as pd


def total_return(
    initial_cash,
    final_value
):

    return (
        (final_value - initial_cash)
        / initial_cash
    ) * 100


def win_rate(
    trade_log
):

    profits = []

    buy_price = None

    for trade in trade_log:

        if trade["Type"] == "BUY":
            buy_price = trade["Price"]

        elif trade["Type"] == "SELL" and buy_price is not None:

            profits.append(
                trade["Price"] - buy_price
            )

            buy_price = None

    if len(profits) == 0:
        return 0

    wins = sum(
        1 for p in profits
        if p > 0
    )

    return (
        wins / len(profits)
    ) * 100


def profit_factor(
    trade_log
):

    profits = []

    buy_price = None

    for trade in trade_log:

        if trade["Type"] == "BUY":
            buy_price = trade["Price"]

        elif trade["Type"] == "SELL" and buy_price is not None:

            profits.append(
                trade["Price"] - buy_price
            )

            buy_price = None

    gross_profit = sum(
        p for p in profits
        if p > 0
    )

    gross_loss = abs(
        sum(
            p for p in profits
            if p < 0
        )
    )

    if gross_loss == 0:
        return float("inf")

    return gross_profit / gross_loss


def max_drawdown(
    equity_curve
):

    equity_curve = np.array(
        equity_curve
    )

    running_max = np.maximum.accumulate(
        equity_curve
    )

    drawdowns = (
        equity_curve
        - running_max
    ) / running_max

    return abs(
        drawdowns.min()
    ) * 100


def sharpe_ratio(
    equity_curve,
    risk_free_rate=0.02
):

    equity_curve = pd.Series(
        equity_curve
    )

    returns = (
        equity_curve
        .pct_change()
        .dropna()
    )

    if returns.std() == 0:
        return 0

    annual_return = (
        returns.mean()
        * 252
    )

    annual_volatility = (
        returns.std()
        * np.sqrt(252)
    )

    return (
        annual_return
        - risk_free_rate
    ) / annual_volatility