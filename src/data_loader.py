import os
import pandas as pd
import yfinance as yf


def download_data(
    ticker: str,
    start_date: str,
    end_date: str
) -> pd.DataFrame:
    """
    Download historical stock data from Yahoo Finance.

    Parameters
    ----------
    ticker : str
        Stock symbol (e.g. AAPL)
    start_date : str
        Format: YYYY-MM-DD
    end_date : str
        Format: YYYY-MM-DD

    Returns
    -------
    pd.DataFrame
        Historical OHLCV data
    """

    df = yf.download(
        ticker,
        start=start_date,
        end=end_date,
        auto_adjust=True
    )

    if df.empty:
        raise ValueError(
            f"No data found for ticker {ticker}"
        )

    return df


def save_data(
    df: pd.DataFrame,
    filepath: str
) -> None:
    """
    Save dataframe to CSV.
    """

    os.makedirs(
        os.path.dirname(filepath),
        exist_ok=True
    )

    df.to_csv(filepath)


def load_data(
    filepath: str
) -> pd.DataFrame:
    """
    Load dataframe from CSV.
    """

    if not os.path.exists(filepath):
        raise FileNotFoundError(
            f"{filepath} does not exist"
        )

    df = pd.read_csv(
        filepath,
        skiprows=[1],
        index_col=0,
        parse_dates=True
    )

    return df


def get_data(
    ticker: str,
    start_date: str,
    end_date: str,
    use_cache: bool = True
) -> pd.DataFrame:
    """
    Uses cached data if available.
    Otherwise downloads and saves.
    """

    filepath = f"data/{ticker}.csv"

    if use_cache and os.path.exists(filepath):
        print(f"Loading cached data: {ticker}")
        return load_data(filepath)

    print(f"Downloading data: {ticker}")

    df = download_data(
        ticker,
        start_date,
        end_date
    )

    save_data(
        df,
        filepath
    )

    return df