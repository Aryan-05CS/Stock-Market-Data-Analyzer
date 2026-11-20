"""Save reproducible stock-price and return charts."""

from pathlib import Path
from typing import Dict

import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns


def create_charts(
    data: pd.DataFrame,
    ticker: str,
    output_dir: Path,
) -> Dict[str, Path]:
    """Create and save price, moving-average, return, and return-distribution charts."""
    output_dir.mkdir(parents=True, exist_ok=True)
    symbol = ticker.strip().upper().replace("/", "_")
    paths = {
        "price": output_dir / "{}_closing_price.png".format(symbol),
        "moving_averages": output_dir / "{}_moving_averages.png".format(symbol),
        "daily_returns": output_dir / "{}_daily_returns.png".format(symbol),
        "return_distribution": output_dir / "{}_return_distribution.png".format(symbol),
    }
    sns.set_theme(style="whitegrid")

    fig, axis = plt.subplots(figsize=(11, 5))
    axis.plot(data.index, data["Analysis Price"], color="#1769aa", linewidth=1.6)
    axis.set(title="{} adjusted closing price".format(symbol), xlabel="Date", ylabel="Price")
    fig.tight_layout()
    fig.savefig(paths["price"], dpi=160)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(11, 5))
    axis.plot(data.index, data["Analysis Price"], label="Adjusted close / close", alpha=0.7)
    for column in ("SMA 20", "SMA 50", "SMA 200"):
        if column in data.columns:
            axis.plot(data.index, data[column], label=column, linewidth=1.4)
    axis.set(title="{} price and moving averages".format(symbol), xlabel="Date", ylabel="Price")
    axis.legend()
    fig.tight_layout()
    fig.savefig(paths["moving_averages"], dpi=160)
    plt.close(fig)

    returns = data["Daily Return"].dropna()
    fig, axis = plt.subplots(figsize=(11, 4))
    axis.plot(returns.index, returns * 100, color="#e67e22", linewidth=0.9)
    axis.axhline(0, color="black", linewidth=0.8)
    axis.set(title="{} daily returns".format(symbol), xlabel="Date", ylabel="Return (%)")
    fig.tight_layout()
    fig.savefig(paths["daily_returns"], dpi=160)
    plt.close(fig)

    fig, axis = plt.subplots(figsize=(9, 4))
    if not returns.empty:
        sns.histplot(returns * 100, bins=30, kde=len(returns) > 1, ax=axis, color="#2a9d8f")
    axis.set(title="{} daily return distribution".format(symbol), xlabel="Daily return (%)")
    fig.tight_layout()
    fig.savefig(paths["return_distribution"], dpi=160)
    plt.close(fig)
    return paths
