import pandas as pd

from src.data_loader import get_data

from src.indicators import sma, ema, rsi, macd, bollinger_bands

from src.strategies import (
    SMACrossoverStrategy,
    RSIStrategy,
    MACDStrategy,
    BollingerStrategy,
    PriceAboveSMAStrategy,
    EMACrossoverStrategy,
)

from src.backtester import Backtester

from src.metrics import total_return, win_rate, max_drawdown, sharpe_ratio

from src.reporting import save_dataframe

from src.visualization import plot_multi_ticker_results


def add_indicators(df):

    df["SMA10"] = sma(df, 10)
    df["SMA50"] = sma(df, 50)

    df["EMA20"] = ema(df, 20)
    df["EMA100"] = ema(df, 100)

    df["RSI"] = rsi(df)

    macd_line, signal_line, histogram = macd(df)

    df["MACD"] = macd_line
    df["MACD_SIGNAL"] = signal_line
    df["MACD_HIST"] = histogram

    upper, middle, lower = bollinger_bands(df)

    df["BB_UPPER"] = upper
    df["BB_MIDDLE"] = middle
    df["BB_LOWER"] = lower

    return df


def main():

    tickers = ["AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META"]

    strategies = {
        "SMA Crossover": SMACrossoverStrategy(),
        "RSI": RSIStrategy(),
        "MACD": MACDStrategy(),
        "Bollinger": BollingerStrategy(),
        "Price > SMA50": PriceAboveSMAStrategy(),
        "EMA Crossover": EMACrossoverStrategy(),
    }

    strategy_results = {}

    for strategy_name in strategies.keys():
        strategy_results[strategy_name] = {
            "returns": [],
            "sharpes": [],
            "drawdowns": [],
            "win_rates": [],
        }

    backtester = Backtester(initial_cash=100000)

    for ticker in tickers:
        print(f"\nTesting {ticker}...")

        df = get_data(ticker=ticker, start_date="2021-01-01", end_date="2026-01-01")

        df = add_indicators(df)

        for strategy_name, strategy in strategies.items():
            signals = strategy.generate_signals(df)

            results = backtester.run(df, signals)

            portfolio_return = total_return(
                results["initial_cash"], results["final_value"]
            )

            wr = win_rate(results["trade_log"])

            mdd = max_drawdown(results["equity_curve"])

            sharpe = sharpe_ratio(results["equity_curve"])

            strategy_results[strategy_name]["returns"].append(portfolio_return)

            strategy_results[strategy_name]["sharpes"].append(sharpe)

            strategy_results[strategy_name]["drawdowns"].append(mdd)

            strategy_results[strategy_name]["win_rates"].append(wr)

    leaderboard = []

    for strategy_name, data in strategy_results.items():
        avg_return = sum(data["returns"]) / len(data["returns"])

        avg_sharpe = sum(data["sharpes"]) / len(data["sharpes"])

        avg_drawdown = sum(data["drawdowns"]) / len(data["drawdowns"])

        avg_win_rate = sum(data["win_rates"]) / len(data["win_rates"])

        leaderboard.append(
            {
                "Strategy": strategy_name,
                "Return": avg_return,
                "Sharpe": avg_sharpe,
                "Drawdown": avg_drawdown,
                "Win Rate": avg_win_rate,
            }
        )

    leaderboard.sort(key=lambda x: x["Return"], reverse=True)

    leaderboard_df = pd.DataFrame(leaderboard)

    save_dataframe(leaderboard_df, "multi_ticker_results.csv")
    plot_multi_ticker_results(leaderboard_df)

    print("\n")
    print("=" * 120)
    print("MULTI-TICKER STRATEGY LEADERBOARD")
    print("=" * 120)

    print(
        f"{'Rank':<6}"
        f"{'Strategy':<20}"
        f"{'Avg Return %':<15}"
        f"{'Avg Sharpe':<15}"
        f"{'Avg Drawdown %':<18}"
        f"{'Avg Win Rate %':<18}"
    )

    print("-" * 120)

    for rank, result in enumerate(leaderboard, start=1):
        print(
            f"{rank:<6}"
            f"{result['Strategy']:<20}"
            f"{result['Return']:<15.2f}"
            f"{result['Sharpe']:<15.2f}"
            f"{result['Drawdown']:<18.2f}"
            f"{result['Win Rate']:<18.2f}"
        )


if __name__ == "__main__":
    main()
