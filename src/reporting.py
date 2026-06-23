import os
import pandas as pd


def sanitize_filename(filename):

    invalid_chars = '<>:"/\\|?*'

    for char in invalid_chars:
        filename = filename.replace(char, "_")

    return filename


def save_trade_log(trade_log, filename="trade_log.csv"):

    os.makedirs("results", exist_ok=True)

    filename = sanitize_filename(filename)

    df = pd.DataFrame(trade_log)

    path = os.path.join("results", filename)

    df.to_csv(path, index=False)

    print(f"Saved: {path}")


def save_metrics(metrics, filename="metrics.csv"):

    os.makedirs("results", exist_ok=True)

    filename = sanitize_filename(filename)

    df = pd.DataFrame([metrics])

    path = os.path.join("results", filename)

    df.to_csv(path, index=False)

    print(f"Saved: {path}")


def save_dataframe(df, filename):

    os.makedirs("results", exist_ok=True)

    filename = sanitize_filename(filename)

    path = os.path.join("results", filename)

    df.to_csv(path, index=False)

    print(f"Saved: {path}")
