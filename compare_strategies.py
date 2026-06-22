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

from src.metrics import (
    total_return,
    win_rate,
    profit_factor,
    max_drawdown,
    sharpe_ratio,
)

from src.benchmark import buy_and_hold_return

from src.reporting import save_trade_log, save_metrics, save_dataframe

from src.visualization import plot_equity_curve, plot_drawdown, plot_strategy_returns


def main():

    df = get_data(ticker="AAPL", start_date="2021-01-01", end_date="2026-01-01")

    benchmark = buy_and_hold_return(df)

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

    strategies = {
        "SMA Crossover": SMACrossoverStrategy(),
        "RSI": RSIStrategy(),
        "MACD": MACDStrategy(),
        "Bollinger": BollingerStrategy(),
        "Price Above SMA50": PriceAboveSMAStrategy(),
        "EMA Crossover": EMACrossoverStrategy(),
    }

    backtester = Backtester(initial_cash=100000)

    strategy_results = []

    for strategy_name, strategy in strategies.items():
        print(f"\nRunning: {strategy_name}")

        signals = strategy.generate_signals(df)

        results = backtester.run(df, signals)

        portfolio_return = total_return(results["initial_cash"], results["final_value"])

        wr = win_rate(results["trade_log"])

        pf = profit_factor(results["trade_log"])

        mdd = max_drawdown(results["equity_curve"])

        sharpe = sharpe_ratio(results["equity_curve"])

        alpha = portfolio_return - benchmark["return"]

        safe_name = (
            strategy_name.replace(" ", "_")
            .replace(">", "GT")
            .replace("<", "LT")
            .replace("/", "_")
            .replace("\\", "_")
            .replace(":", "_")
            .replace("*", "_")
            .replace("?", "_")
            .replace('"', "_")
            .replace("|", "_")
        )

        save_trade_log(results["trade_log"], f"{safe_name}_trade_log.csv")

        save_metrics(
            {
                "Return": portfolio_return,
                "Alpha": alpha,
                "Sharpe": sharpe,
                "Drawdown": mdd,
                "Win Rate": wr,
                "Profit Factor": pf,
                "Trades": len(results["trade_log"]),
            },
            f"{safe_name}_metrics.csv",
        )

        plot_equity_curve(results["equity_curve"], safe_name)

        plot_drawdown(results["equity_curve"], safe_name)

        strategy_results.append(
            {
                "Strategy": strategy_name,
                "Return": portfolio_return,
                "Alpha": alpha,
                "Win Rate": wr,
                "Profit Factor": pf,
                "Drawdown": mdd,
                "Sharpe": sharpe,
                "Trades": len(results["trade_log"]),
            }
        )

    strategy_results.sort(key=lambda x: x["Return"], reverse=True)

    strategy_df = pd.DataFrame(strategy_results)

    save_dataframe(strategy_df, "strategy_leaderboard.csv")

    plot_strategy_returns(strategy_df)

    print("\n")
    print("=" * 60)
    print("BUY & HOLD BENCHMARK")
    print("=" * 60)

    print(f"Final Value : ${benchmark['final_value']:.2f}")

    print(f"Return      : {benchmark['return']:.2f}%")

    print("\n")
    print("=" * 140)
    print("STRATEGY LEADERBOARD")
    print("=" * 140)

    print(
        f"{'Rank':<6}"
        f"{'Strategy':<25}"
        f"{'Return %':<12}"
        f"{'Alpha %':<12}"
        f"{'Sharpe':<12}"
        f"{'Drawdown %':<15}"
        f"{'Win Rate %':<15}"
        f"{'Trades':<10}"
    )

    print("-" * 140)

    for rank, result in enumerate(strategy_results, start=1):
        print(
            f"{rank:<6}"
            f"{result['Strategy']:<25}"
            f"{result['Return']:<12.2f}"
            f"{result['Alpha']:<12.2f}"
            f"{result['Sharpe']:<12.2f}"
            f"{result['Drawdown']:<15.2f}"
            f"{result['Win Rate']:<15.2f}"
            f"{result['Trades']:<10}"
        )


if __name__ == "__main__":
    main()
