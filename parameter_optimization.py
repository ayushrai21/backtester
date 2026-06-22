import pandas as pd
from src.data_loader import get_data
from src.indicators import sma
from src.strategies import SMACrossoverStrategy
from src.backtester import Backtester
from src.metrics import total_return, sharpe_ratio, max_drawdown
from src.reporting import save_dataframe
from src.visualization import plot_sma_heatmap


def main():

    df = get_data(ticker="AAPL", start_date="2021-01-01", end_date="2026-01-01")

    fast_periods = [5, 10, 15, 20]
    slow_periods = [20, 50, 100, 200]
    all_periods = set(fast_periods + slow_periods)

    for period in all_periods:
        df[f"SMA{period}"] = sma(df, period)

    backtester = Backtester(initial_cash=100000)
    results = []

    for fast in fast_periods:
        for slow in slow_periods:
            if fast >= slow:
                continue
            strategy = SMACrossoverStrategy(fast_period=fast, slow_period=slow)
            signals = strategy.generate_signals(df)
            backtest = backtester.run(df, signals)
            portfolio_return = total_return(
                backtest["initial_cash"], backtest["final_value"]
            )
            sharpe = sharpe_ratio(backtest["equity_curve"])
            drawdown = max_drawdown(backtest["equity_curve"])

            results.append(
                {
                    "Fast SMA": fast,
                    "Slow SMA": slow,
                    "Return": portfolio_return,
                    "Sharpe": sharpe,
                    "Drawdown": drawdown,
                }
            )

    results.sort(key=lambda x: x["Return"], reverse=True)
    results_df = pd.DataFrame(results)
    save_dataframe(results_df, "optimization_results.csv")
    plot_sma_heatmap(results_df)

    print("\n")
    print("=" * 90)
    print("SMA PARAMETER OPTIMIZATION")
    print("=" * 90)

    print(
        f"{'Rank':<6}"
        f"{'Fast':<10}"
        f"{'Slow':<10}"
        f"{'Return %':<15}"
        f"{'Sharpe':<15}"
        f"{'Drawdown %':<15}"
    )

    print("-" * 90)

    for rank, result in enumerate(results, start=1):
        print(
            f"{rank:<6}"
            f"{result['Fast SMA']:<10}"
            f"{result['Slow SMA']:<10}"
            f"{result['Return']:<15.2f}"
            f"{result['Sharpe']:<15.2f}"
            f"{result['Drawdown']:<15.2f}"
        )


if __name__ == "__main__":
    main()
