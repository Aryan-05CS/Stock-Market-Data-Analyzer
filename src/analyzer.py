"""Calculate price indicators and descriptive risk/return statistics."""

import math
from typing import Dict, Iterable, Tuple

import numpy as np
import pandas as pd


def analyze_stock_data(
    data: pd.DataFrame,
    ticker: str,
    moving_average_windows: Iterable[int] = (20, 50, 200),
) -> Tuple[pd.DataFrame, Dict[str, object]]:
    """Calculate daily returns, moving averages, volatility, and summary metrics."""
    if "Analysis Price" not in data.columns or data.empty:
        raise ValueError("Provide non-empty cleaned stock data to analyze.")

    result = data.copy().sort_index()
    price = result["Analysis Price"].astype(float)
    result["Daily Return"] = price.pct_change()

    windows = tuple(moving_average_windows)
    if any(window <= 0 for window in windows):
        raise ValueError("Moving-average windows must be positive integers.")
    for window in windows:
        result["SMA {}".format(window)] = price.rolling(
            window=window, min_periods=window
        ).mean()

    returns = result["Daily Return"].dropna()
    volatility = (
        float(returns.std(ddof=1) * math.sqrt(252))
        if len(returns) > 1
        else float("nan")
    )
    cumulative_returns = (1 + returns).cumprod()
    initial_value = pd.Series([1.0], index=[result.index[0]])
    cumulative_returns = pd.concat([initial_value, cumulative_returns])
    running_peak = cumulative_returns.cummax()
    drawdown = cumulative_returns / running_peak - 1

    latest = result.iloc[-1]
    short_sma = latest.get("SMA 20", np.nan)
    long_sma = latest.get("SMA 50", np.nan)
    if pd.notna(short_sma) and pd.notna(long_sma):
        if short_sma > long_sma:
            trend = "The 20-session average is above the 50-session average."
        elif short_sma < long_sma:
            trend = "The 20-session average is below the 50-session average."
        else:
            trend = "The 20-session and 50-session averages are equal."
    else:
        trend = "Insufficient history for a 20/50-session moving-average comparison."

    high_values = result["High"].dropna() if "High" in result.columns else price
    low_values = result["Low"].dropna() if "Low" in result.columns else price
    if high_values.empty:
        high_values = price
    if low_values.empty:
        low_values = price
    high = high_values.max()
    low = low_values.min()
    high_date = high_values.idxmax()
    low_date = low_values.idxmin()

    summary: Dict[str, object] = {
        "ticker": ticker.strip().upper(),
        "start_date": result.index[0],
        "end_date": result.index[-1],
        "observations": len(result),
        "start_price": float(price.iloc[0]),
        "latest_price": float(price.iloc[-1]),
        "total_return": float(price.iloc[-1] / price.iloc[0] - 1),
        "annualized_volatility": volatility,
        "max_drawdown": float(drawdown.min()) if not drawdown.empty else float("nan"),
        "highest_price": float(high),
        "highest_price_date": high_date,
        "lowest_price": float(low),
        "lowest_price_date": low_date,
        "trend": trend,
    }
    return result, summary
