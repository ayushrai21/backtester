import os
import pandas as pd
import matplotlib.pyplot as plt

RESULTS_DIR = "results"

os.makedirs(RESULTS_DIR, exist_ok=True)


def plot_equity_curve(equity_curve, strategy_name):
    plt.figure(figsize=(12, 6))
    plt.plot(equity_curve, linewidth=2)
    plt.title(f"{strategy_name} Equity Curve")
    plt.xlabel("Days")
    plt.ylabel("Portfolio Value ($)")
    plt.grid(True)

    filename = f"{strategy_name}".replace(" ", "_") + "_equity_curve.png"

    plt.savefig(os.path.join(RESULTS_DIR, filename), bbox_inches="tight")
    plt.close()

    print(f"Saved: results/{filename}")


def plot_drawdown(equity_curve, strategy_name):

    equity = pd.Series(equity_curve)

    running_max = equity.cummax()

    drawdown = ((equity - running_max) / running_max) * 100

    plt.figure(figsize=(12, 6))
    plt.plot(drawdown, linewidth=2)
    plt.title(f"{strategy_name} Drawdown")
    plt.xlabel("Days")
    plt.ylabel("Drawdown (%)")
    plt.grid(True)

    filename = f"{strategy_name}".replace(" ", "_") + "_drawdown.png"

    plt.savefig(os.path.join(RESULTS_DIR, filename), bbox_inches="tight")
    plt.close()

    print(f"Saved: results/{filename}")


def plot_strategy_returns(leaderboard_df):

    df = leaderboard_df.sort_values("Return", ascending=False)

    plt.figure(figsize=(12, 6))

    plt.bar(df["Strategy"], df["Return"])

    plt.title("Strategy Comparison")

    plt.xlabel("Strategy")

    plt.ylabel("Return (%)")

    plt.xticks(rotation=30)

    plt.grid(axis="y")

    filename = "strategy_comparison.png"

    plt.savefig(os.path.join(RESULTS_DIR, filename), bbox_inches="tight")

    plt.close()

    print(f"Saved: results/{filename}")


def plot_multi_ticker_results(leaderboard_df):

    df = leaderboard_df.sort_values("Return", ascending=False)

    plt.figure(figsize=(12, 6))

    plt.bar(df["Strategy"], df["Return"])

    plt.title("Multi-Ticker Strategy Comparison")

    plt.xlabel("Strategy")

    plt.ylabel("Average Return (%)")

    plt.xticks(rotation=30)

    plt.grid(axis="y")

    plt.savefig(
        os.path.join(RESULTS_DIR, "multi_ticker_comparison.png"), bbox_inches="tight"
    )

    plt.close()

    print("Saved: results/multi_ticker_comparison.png")


def plot_sma_heatmap(optimization_df):

    heatmap = optimization_df.pivot(
        index="Fast SMA", columns="Slow SMA", values="Return"
    )

    plt.figure(figsize=(10, 8))
    plt.imshow(heatmap, aspect="auto")
    plt.colorbar(label="Return (%)")
    plt.xticks(range(len(heatmap.columns)), heatmap.columns)
    plt.yticks(range(len(heatmap.index)), heatmap.index)

    for i in range(len(heatmap.index)):
        for j in range(len(heatmap.columns)):
            value = heatmap.iloc[i, j]
            if not pd.isna(value):
                plt.text(j, i, f"{value:.1f}", ha="center", va="center")

    plt.xlabel("Slow SMA")
    plt.ylabel("Fast SMA")
    plt.title("SMA Parameter Optimization Heatmap")
    plt.savefig(os.path.join(RESULTS_DIR, "sma_heatmap.png"), bbox_inches="tight")
    plt.close()

    print("Saved: results/sma_heatmap.png")
