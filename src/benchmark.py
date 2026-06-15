# src/benchmark.py

def buy_and_hold_return(
    df,
    initial_cash=100000
):

    first_price = df["Close"].iloc[0]

    last_price = df["Close"].iloc[-1]

    shares = initial_cash // first_price

    remaining_cash = (
        initial_cash
        - shares * first_price
    )

    final_value = (
        remaining_cash
        + shares * last_price
    )

    total_return = (
        (final_value - initial_cash)
        / initial_cash
    ) * 100

    return {
        "final_value": final_value,
        "return": total_return
    }