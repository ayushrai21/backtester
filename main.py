from src.data_loader import get_data

from src.indicators import sma, ema, rsi, macd, bollinger_bands

from src.strategies import (
    SMACrossoverStrategy,
)

from src.backtester import Backtester

from src.metrics import (
    total_return,
    win_rate,
    profit_factor,
    max_drawdown,
    sharpe_ratio,
)


def main():

    df = get_data(ticker="AAPL", start_date="2021-01-01", end_date="2026-01-01")

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

    strategy = SMACrossoverStrategy()

    # strategy = RSIStrategy()
    # strategy = MACDStrategy()
    # strategy = BollingerStrategy()
    # strategy = PriceAboveSMAStrategy()
    # strategy = EMACrossoverStrategy()

    signals = strategy.generate_signals(df)

    backtester = Backtester(initial_cash=100000)

    results = backtester.run(df, signals)

    portfolio_return = total_return(results["initial_cash"], results["final_value"])

    wr = win_rate(results["trade_log"])

    pf = profit_factor(results["trade_log"])

    mdd = max_drawdown(results["equity_curve"])

    sharpe = sharpe_ratio(results["equity_curve"])

    print("\n" + "=" * 50)
    print("BACKTEST RESULTS")
    print("=" * 50)

    print(f"Initial Capital : ${results['initial_cash']:.2f}")

    print(f"Final Capital   : ${results['final_value']:.2f}")

    print(f"Total Profit    : ${results['profit']:.2f}")

    print(f"Total Return    : {portfolio_return:.2f}%")

    print(f"Win Rate        : {wr:.2f}%")

    print(f"Profit Factor   : {pf:.2f}")

    print(f"Max Drawdown    : {mdd:.2f}%")

    print(f"Sharpe Ratio    : {sharpe:.2f}")

    print(f"Total Trades    : {len(results['trade_log'])}")

    print("\n" + "=" * 50)

    print("\nSignal Counts")

    print(f"BUY  Signals : {signals.count(1)}")

    print(f"SELL Signals : {signals.count(-1)}")

    print(f"HOLD Signals : {signals.count(0)}")

    print("\nFirst 10 Trades")

    for trade in results["trade_log"][:10]:
        print(trade)

    print("\nLast 5 Portfolio Values")

    for value in results["equity_curve"][-5:]:
        print(round(value, 2))


if __name__ == "__main__":
    main()
