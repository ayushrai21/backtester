import streamlit as st
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

st.set_page_config(page_title="Quant Research Platform", layout="wide")

st.title("Quant Research & Backtesting Platform")

st.sidebar.header("Backtest Settings")

ticker = st.sidebar.selectbox(
    "Ticker", ["AAPL", "MSFT", "NVDA", "GOOG", "AMZN", "META"]
)

strategy_name = st.sidebar.selectbox(
    "Strategy",
    ["SMA Crossover", "EMA Crossover", "RSI", "MACD", "Bollinger", "Price Above SMA50"],
)

initial_cash = st.sidebar.number_input("Initial Capital", value=100000)

run_backtest = st.sidebar.button("Run Backtest")


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


def get_strategy(name):

    strategies = {
        "SMA Crossover": SMACrossoverStrategy(),
        "EMA Crossover": EMACrossoverStrategy(),
        "RSI": RSIStrategy(),
        "MACD": MACDStrategy(),
        "Bollinger": BollingerStrategy(),
        "Price Above SMA50": PriceAboveSMAStrategy(),
    }

    return strategies[name]


if run_backtest:
    with st.spinner("Running backtest..."):
        df = get_data(ticker=ticker, start_date="2021-01-01", end_date="2026-01-01")

        df = add_indicators(df)

        strategy = get_strategy(strategy_name)

        signals = strategy.generate_signals(df)

        backtester = Backtester(initial_cash=initial_cash)

        results = backtester.run(df, signals)

        portfolio_return = total_return(results["initial_cash"], results["final_value"])

        wr = win_rate(results["trade_log"])

        pf = profit_factor(results["trade_log"])

        mdd = max_drawdown(results["equity_curve"])

        sharpe = sharpe_ratio(results["equity_curve"])

    col1, col2, col3, col4, col5 = st.columns(5)

    col1.metric("Return %", f"{portfolio_return:.2f}")

    col2.metric("Sharpe", f"{sharpe:.2f}")

    col3.metric("Drawdown %", f"{mdd:.2f}")

    col4.metric("Win Rate %", f"{wr:.2f}")

    col5.metric("Profit Factor", f"{pf:.2f}")

    st.divider()

    st.subheader("Equity Curve")

    equity_df = pd.DataFrame({"Portfolio Value": results["equity_curve"]})

    st.line_chart(equity_df)

    equity = pd.Series(results["equity_curve"])

    running_max = equity.cummax()

    drawdown = ((equity - running_max) / running_max) * 100

    st.subheader("Drawdown Curve")

    st.line_chart(drawdown)

    st.subheader("Trade Log")

    trade_df = pd.DataFrame(results["trade_log"])

    st.dataframe(trade_df, use_container_width=True)

    with st.expander("View Price Data"):
        st.dataframe(df.tail(100), use_container_width=True)
