import os
import pandas as pd
import yfinance as yf

DATA_DIR = "data"


def download_data(ticker, start_date, end_date):
    print(f"Downloading data: {ticker}")
    df = yf.download(
        ticker, start=start_date, end=end_date, auto_adjust=True, progress=True
    )
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.get_level_values(0)
    return df


def save_data(df, ticker):
    os.makedirs(DATA_DIR, exist_ok=True)
    filepath = os.path.join(DATA_DIR, f"{ticker}.csv")
    df.to_csv(filepath)


def load_data(ticker):
    filepath = os.path.join(DATA_DIR, f"{ticker}.csv")
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)

    df = df.dropna()

    numeric_cols = ["Open", "High", "Low", "Close", "Volume"]

    for col in numeric_cols:
        if col in df.columns:
            df[col] = pd.to_numeric(df[col], errors="coerce")

    df = df.dropna()
    return df


def get_data(ticker, start_date, end_date):
    filepath = os.path.join(DATA_DIR, f"{ticker}.csv")
    if os.path.exists(filepath):
        print(f"Loading cached data: {ticker}")
        return load_data(ticker)

    df = download_data(ticker, start_date, end_date)

    save_data(df, ticker)
    return df
